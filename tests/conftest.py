# -*- coding: utf-8 -*-
"""
EcoWater HydroLink Test Configuration

Provides shared test configuration and fixtures for all HydroLink tests.

Author: GrumpyTanker + AI
Created: June 12, 2025
Updated: October 2, 2025

Changelog:
- 0.1.0 (2025-06-12)
  * Initial release
  * Basic test configuration

- 0.2.0 (2025-10-02)
  * Added socket disabling
  * Improved test isolation

License: MIT
See LICENSE file in the project root for full license information.
"""

import asyncio
import contextlib
import os
from unittest.mock import AsyncMock, Mock, patch
import pytest
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from pytest_socket import disable_socket, enable_socket


@pytest.fixture(autouse=True)
def disable_socket_for_tests():
    """Disable socket usage for most tests."""
    with contextlib.suppress(Exception):
        disable_socket()
    return True


import asyncio


class MockEventLoop(asyncio.AbstractEventLoop):
    """A mock event loop for testing."""

    def __init__(self):
        self.run_in_executor = AsyncMock()
        self.create_task = Mock()
        self.set_debug = Mock()
        self.run_until_complete = Mock()
        self.close = Mock()

    def get_debug(self):
        return False

    def create_future(self):
        fut = asyncio.Future()
        fut.set_result(None)
        return fut

    def call_soon(self, callback, *args, context=None):
        callback(*args)
        return None

    def is_running(self):
        return True

    def is_closed(self):
        return False

    def stop(self):
        pass

    def call_exception_handler(self, context):
        pass

    def default_exception_handler(self, context):
        pass

    def call_soon_threadsafe(self, callback, *args):
        return self.call_soon(callback, *args)

    def get_exception_handler(self):
        return None

    def set_exception_handler(self, handler):
        pass


@pytest.fixture
def mock_event_loop():
    """Create a mock event loop for use in tests."""
    loop = MockEventLoop()
    asyncio.set_event_loop(loop)
    return loop


@pytest.fixture
def hass(mock_event_loop):
    """Create mock Home Assistant instance for testing."""
    hass = Mock(spec=HomeAssistant)
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {
        "integrations": {},  # Required for async_setup_component
        "device_registry": {},  # May be needed
        "entity_registry": {},  # May be needed
    }
    hass.config.components = set()

    # Mock core services
    hass.services = Mock()
    hass.services.async_register = AsyncMock()

    # Mock async methods
    hass.async_add_executor_job = AsyncMock()
    hass.config_entries = Mock()
    hass.config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
    hass.config_entries.async_forward_entry_unload = AsyncMock(return_value=True)
    hass.config_entries.async_unload_platforms = AsyncMock(return_value=True)
    hass.config_entries.async_entries = AsyncMock(return_value=[])
    hass.config_entries.async_flow_progress = AsyncMock(return_value=[])

    # Set up loop
    hass.loop = mock_event_loop

    return hass
