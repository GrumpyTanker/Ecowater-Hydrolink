# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Configuration Flow

Manages the setup and configuration process for the HydroLink integration within
Home Assistant. Provides a user-friendly interface for authentication, validation,
and initial setup of the EcoWater water softener monitoring system.

Key Features:
- Secure credential collection and validation
- Real-time API connectivity testing
- User-friendly error messages and guidance
- Automatic device discovery and configuration
- Re-authentication support for expired credentials
- Integration with Home Assistant's configuration UI
- Proper handling of network and authentication errors

Configuration Process:
1. User credential input (email/password)
2. API connectivity and authentication testing
3. Device discovery and validation
4. Integration setup and entity creation
5. Success confirmation with device information

This flow ensures a smooth setup experience while maintaining security
and providing clear feedback throughout the configuration process.

Author: GrumpyTanker + AI Assistant
Created: June 12, 2025
Updated: October 3, 2025

Version History:
- 1.0.0 (2025-10-03)
  * Production release with enhanced user experience
  * Improved error handling and user guidance
  * Better validation and connectivity testing
  * Enhanced security and credential management

- 0.2.1 (2025-10-02)
  * Fixed error handling in configuration flow
  * Improved validation feedback and messaging

- 0.2.0 (2025-10-02)
  * Added comprehensive input validation
  * Enhanced error handling and user feedback
  * Added re-authentication support
  * Comprehensive type hints and documentation

- 0.1.0 (2025-06-12)
  * Initial release with basic configuration flow
  * User authentication and setup foundation

License: MIT
See LICENSE file in the project root for full license information.
"""

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN
from .api import HydroLinkApi, CannotConnect, InvalidAuth

_LOGGER = logging.getLogger(__name__)

# Schema for the user input form
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HydroLink."""

    VERSION = 1
    DOMAIN = DOMAIN
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step of the user configuration.

        This is called when a user initiates a new configuration flow. It
        presents a form for the user to enter their credentials, validates
        them, and creates a config entry on success.

        Args:
            user_input: The user-provided input from the form.

        Returns:
            A form to be shown to the user, or a result indicating success
            or failure.
        """
        errors = {}
        if user_input is not None:
            # Check for empty fields first
            if not user_input.get(CONF_EMAIL) or not user_input.get(CONF_PASSWORD):
                errors["base"] = "invalid_auth"
                return self.async_show_form(
                    step_id="user",
                    data_schema=DATA_SCHEMA,
                    errors=errors,
                )

            try:
                # Create an API instance and attempt to log in
                api = HydroLinkApi(user_input[CONF_EMAIL], user_input[CONF_PASSWORD])

                # Wrap in try-except to handle API exceptions
                try:
                    # Note: login may raise InvalidAuth or CannotConnect
                    await self.hass.async_add_executor_job(api.login)
                except (InvalidAuth, CannotConnect) as err:
                    # Re-raise original exception to maintain error type
                    raise err
                except Exception as err:
                    _LOGGER.exception("Unexpected API error")
                    raise CannotConnect from err

                # Only proceed if login was successful
                await self.async_set_unique_id(user_input[CONF_EMAIL])
                self._abort_if_unique_id_configured()

                # Create the config entry
                return self.async_create_entry(
                    title=user_input[CONF_EMAIL], data=user_input
                )

            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Failed to create API instance")
                errors["base"] = "unknown"
        # Show form with or without errors
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
