"""Unit tests for the HydroLink services."""

from unittest.mock import AsyncMock, Mock, patch
import pytest
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.const import ATTR_DEVICE_ID
from homeassistant.helpers import device_registry as dr

from custom_components.hydrolink.services import async_setup_services
from custom_components.hydrolink.const import DOMAIN, SERVICE_TRIGGER_REGENERATION
from custom_components.hydrolink.api import CannotConnect, InvalidAuth


@pytest.fixture
def mock_device_registry():
    """Create a mock device registry."""
    registry = Mock(spec=dr.DeviceRegistry)
    return registry


@pytest.fixture
def mock_device_entry():
    """Create a mock device registry entry."""
    entry = Mock()
    entry.config_entry_id = "test_config_entry_id"
    return entry


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator with API."""
    coordinator = Mock()
    coordinator.api = Mock()
    coordinator.api.trigger_regeneration = Mock()
    return coordinator


@pytest.mark.asyncio
async def test_async_setup_services(hass):
    """Test service setup."""
    hass.services = Mock()
    hass.services.async_register = Mock()

    await async_setup_services(hass)

    # Verify the service was registered
    hass.services.async_register.assert_called_once()
    call_args = hass.services.async_register.call_args

    assert call_args[0][0] == DOMAIN
    assert call_args[0][1] == SERVICE_TRIGGER_REGENERATION
    assert callable(call_args[0][2])  # Service handler function
    assert isinstance(call_args[1]["schema"], vol.Schema)


@pytest.mark.asyncio
async def test_trigger_regeneration_success(
    hass, mock_device_registry, mock_device_entry, mock_coordinator
):
    """Test successful regeneration trigger."""
    device_id = "test_device_id"

    # Setup mocks
    with patch(
        "custom_components.hydrolink.services.dr.async_get",
        return_value=mock_device_registry,
    ):
        with patch(
            "custom_components.hydrolink.services.dr.async_entries_for_device_id",
            return_value=[mock_device_entry],
        ):
            hass.data = {DOMAIN: {"test_config_entry_id": mock_coordinator}}
            hass.async_add_executor_job = AsyncMock()

            await async_setup_services(hass)

            # Get the registered service function
            service_call = hass.services.async_register.call_args[0][2]

            # Create a service call
            call = ServiceCall(
                DOMAIN, SERVICE_TRIGGER_REGENERATION, {ATTR_DEVICE_ID: device_id}
            )

            # Execute the service
            await service_call(call)

            # Verify the API method was called
            hass.async_add_executor_job.assert_called_once()


@pytest.mark.asyncio
async def test_trigger_regeneration_device_not_found(hass, mock_device_registry):
    """Test regeneration trigger with device not found."""
    device_id = "nonexistent_device_id"

    # Setup mocks
    with patch(
        "custom_components.hydrolink.services.dr.async_get",
        return_value=mock_device_registry,
    ):
        with patch(
            "custom_components.hydrolink.services.dr.async_entries_for_device_id",
            return_value=[],
        ):
            await async_setup_services(hass)

            # Get the registered service function
            service_call = hass.services.async_register.call_args[0][2]

            # Create a service call
            call = ServiceCall(
                DOMAIN, SERVICE_TRIGGER_REGENERATION, {ATTR_DEVICE_ID: device_id}
            )

            # Execute the service and expect an error
            with pytest.raises(ValueError, match=f"Device {device_id} not found"):
                await service_call(call)


@pytest.mark.asyncio
async def test_trigger_regeneration_no_config_entry(hass, mock_device_registry):
    """Test regeneration trigger with no config entry."""
    device_id = "test_device_id"

    # Create device entry without config_entry_id
    mock_device_entry = Mock()
    mock_device_entry.config_entry_id = None

    # Setup mocks
    with patch(
        "custom_components.hydrolink.services.dr.async_get",
        return_value=mock_device_registry,
    ):
        with patch(
            "custom_components.hydrolink.services.dr.async_entries_for_device_id",
            return_value=[mock_device_entry],
        ):
            await async_setup_services(hass)

            # Get the registered service function
            service_call = hass.services.async_register.call_args[0][2]

            # Create a service call
            call = ServiceCall(
                DOMAIN, SERVICE_TRIGGER_REGENERATION, {ATTR_DEVICE_ID: device_id}
            )

            # Execute the service and expect an error
            with pytest.raises(
                ValueError, match=f"No config entry found for device {device_id}"
            ):
                await service_call(call)


@pytest.mark.asyncio
async def test_trigger_regeneration_api_error(
    hass, mock_device_registry, mock_device_entry, mock_coordinator
):
    """Test regeneration trigger with API error."""
    device_id = "test_device_id"

    # Setup mocks
    with patch(
        "custom_components.hydrolink.services.dr.async_get",
        return_value=mock_device_registry,
    ):
        with patch(
            "custom_components.hydrolink.services.dr.async_entries_for_device_id",
            return_value=[mock_device_entry],
        ):
            hass.data = {DOMAIN: {"test_config_entry_id": mock_coordinator}}

            # Mock async_add_executor_job to raise an exception
            async def mock_executor_job(func, *args):
                raise CannotConnect("Network error")

            hass.async_add_executor_job = mock_executor_job

            await async_setup_services(hass)

            # Get the registered service function
            service_call = hass.services.async_register.call_args[0][2]

            # Create a service call
            call = ServiceCall(
                DOMAIN, SERVICE_TRIGGER_REGENERATION, {ATTR_DEVICE_ID: device_id}
            )

            # Execute the service and expect an error
            with pytest.raises(ValueError, match="Failed to trigger regeneration"):
                await service_call(call)


@pytest.mark.asyncio
async def test_trigger_regeneration_invalid_auth(
    hass, mock_device_registry, mock_device_entry, mock_coordinator
):
    """Test regeneration trigger with invalid auth error."""
    device_id = "test_device_id"

    # Setup mocks
    with patch(
        "custom_components.hydrolink.services.dr.async_get",
        return_value=mock_device_registry,
    ):
        with patch(
            "custom_components.hydrolink.services.dr.async_entries_for_device_id",
            return_value=[mock_device_entry],
        ):
            hass.data = {DOMAIN: {"test_config_entry_id": mock_coordinator}}

            # Mock async_add_executor_job to raise an InvalidAuth exception
            async def mock_executor_job(func, *args):
                raise InvalidAuth("Authentication failed")

            hass.async_add_executor_job = mock_executor_job

            await async_setup_services(hass)

            # Get the registered service function
            service_call = hass.services.async_register.call_args[0][2]

            # Create a service call
            call = ServiceCall(
                DOMAIN, SERVICE_TRIGGER_REGENERATION, {ATTR_DEVICE_ID: device_id}
            )

            # Execute the service and expect an error
            with pytest.raises(ValueError, match="Failed to trigger regeneration"):
                await service_call(call)
