# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Test Helpers

Provides helper functions and mock objects for testing the HydroLink
integration. Includes mock Home Assistant instance creation and common
test utilities.

Author: GrumpyTanker + AI
Created: June 12, 2025
Updated: October 2, 2025

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release
  * Basic mock helpers

- 0.2.0 (2025-10-02)
  * Added comprehensive mocking
  * Added type hints
  * Improved mock configuration

- 0.2.1 (2025-10-02)
  * Added exception propagation in executor jobs
  * Improved async mock configuration
  * Enhanced test infrastructure reliability

License: MIT
See LICENSE file in the project root for full license information.
"""
from unittest.mock import AsyncMock, Mock, patch

from homeassistant.core import HomeAssistant


def create_mock_hass():
    """Create a mock Home Assistant instance."""
    hass = Mock(spec=HomeAssistant)

    # Mock async_add_executor_job to propagate exceptions
    async def async_exec_with_exc(func, *args, **kwargs):
        """Execute function and propagate exceptions."""
        return func(*args, **kwargs)

    hass.async_add_executor_job = async_exec_with_exc

    # Mock config_entries
    config_entries = Mock()
    config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
    config_entries.async_forward_entry_unload = AsyncMock(return_value=True)
    config_entries.async_unload_platforms = AsyncMock(return_value=True)
    hass.config_entries = config_entries

    # Mock data storage
    hass.data = {}

    # Mock config
    hass.config = Mock()
    hass.config.components = set()

    # Mock services
    hass.services = Mock()
    hass.services.async_register = AsyncMock()

    return hass
