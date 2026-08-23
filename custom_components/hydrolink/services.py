# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Services Platform

Implements service calls for the HydroLink integration, providing user-accessible
control functions for EcoWater water softener devices. Enables manual regeneration
triggering and other device management capabilities through Home Assistant services.

Service Capabilities:
- Manual regeneration initiation for immediate salt treatment
- Device control and management functions
- Integration with Home Assistant automation and scripts
- Comprehensive error handling and validation
- Secure API communication with proper authentication

Available Services:
- trigger_regeneration: Manually start a regeneration cycle
- Future services: Schedule management, maintenance reminders, etc.

This module bridges user actions in Home Assistant with the HydroLink cloud API,
ensuring secure and reliable device control while maintaining proper error handling
and user feedback.

Author: GrumpyTanker + AI Assistant
Created: June 12, 2025
Updated: October 3, 2025

Version History:
- 1.0.0 (2025-10-03)
  * Production release with enhanced service reliability
  * Improved error handling and user feedback
  * Enhanced validation and security measures
  * Better integration with Home Assistant service system

- 0.2.0 (2025-10-02)
  * Added manual regeneration service implementation
  * Improved error handling and validation
  * Added comprehensive type hints
  * Enhanced logging and debugging

- 0.1.0 (2025-06-12)
  * Initial release with basic service framework
  * Service registration and setup infrastructure

License: MIT
See LICENSE file in the project root for full license information.
"""

from typing import Dict, Any
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.const import ATTR_DEVICE_ID
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN, SERVICE_TRIGGER_REGENERATION
from .api import CannotConnect, InvalidAuth


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up HydroLink services."""
    device_registry = dr.async_get(hass)

    async def trigger_regeneration(call: ServiceCall) -> None:
        """Handle the regeneration trigger service call."""
        device_id = call.data[ATTR_DEVICE_ID]

        # Find the correct device entry
        device_entries = dr.async_entries_for_device_id(device_registry, device_id)
        if not device_entries:
            raise ValueError(f"Device {device_id} not found")

        # Get the first config entry ID for this device
        entry_id = next(iter(device_entries)).config_entry_id
        if not entry_id:
            raise ValueError(f"No config entry found for device {device_id}")

        # Get the API instance from the coordinator
        coordinator = hass.data[DOMAIN][entry_id]

        try:
            await hass.async_add_executor_job(
                coordinator.api.trigger_regeneration, device_id
            )
        except (CannotConnect, InvalidAuth) as err:
            raise ValueError(f"Failed to trigger regeneration: {err}") from err

    hass.services.async_register(
        DOMAIN,
        SERVICE_TRIGGER_REGENERATION,
        trigger_regeneration,
        schema=vol.Schema(
            {
                vol.Required(ATTR_DEVICE_ID): str,
            }
        ),
    )
