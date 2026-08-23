"""Unit tests for the HydroLink integration."""

from unittest.mock import AsyncMock, Mock, patch
import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from custom_components.hydrolink import async_setup_entry, async_unload_entry
from custom_components.hydrolink.const import DOMAIN
from custom_components.hydrolink.const import PLATFORMS

# Test data
MOCK_CONFIG = {"email": "test@example.com", "password": "password123"}


@pytest.fixture
def mock_config_entry() -> ConfigEntry:
    """Create a mock config entry."""
    # Handle different Home Assistant versions that may or may not require discovery_keys
    try:
        return ConfigEntry(
            version=1,
            minor_version=1,
            domain=DOMAIN,
            title="HydroLink Test",
            data=MOCK_CONFIG,
            source="user",
            options={},
            unique_id="test@example.com",
            discovery_keys=None,
        )
    except TypeError:
        # Fallback for older HA versions that don't support discovery_keys
        return ConfigEntry(
            version=1,
            minor_version=1,
            domain=DOMAIN,
            title="HydroLink Test",
            data=MOCK_CONFIG,
            source="user",
            options={},
            unique_id="test@example.com",
        )


@pytest.fixture
def mock_coordinator(hass: HomeAssistant, mock_config_entry: ConfigEntry) -> Mock:
    """Create a mock data update coordinator."""
    from custom_components.hydrolink.coordinator import HydroLinkDataUpdateCoordinator

    coordinator = HydroLinkDataUpdateCoordinator(hass, mock_config_entry)
    coordinator.async_setup = Mock(return_value=True)
    coordinator.async_config_entry_first_refresh = AsyncMock()
    return coordinator


@pytest.mark.asyncio
async def test_setup_entry(
    hass: HomeAssistant, mock_config_entry: ConfigEntry, mock_coordinator: Mock
):
    """Test setting up the integration."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {}

    with patch(
        "custom_components.hydrolink.coordinator.HydroLinkDataUpdateCoordinator",
        return_value=mock_coordinator,
    ):
        result = await async_setup_entry(hass, mock_config_entry)

    assert result is True
    assert DOMAIN in hass.data
    assert mock_config_entry.entry_id in hass.data[DOMAIN]
    assert hass.data[DOMAIN][mock_config_entry.entry_id] == mock_coordinator
    hass.config_entries.async_forward_entry_setups.assert_called_once_with(
        mock_config_entry, PLATFORMS
    )


@pytest.mark.asyncio
async def test_unload_entry(
    hass: HomeAssistant, mock_config_entry: ConfigEntry, mock_coordinator: Mock
):
    """Test unloading the integration."""
    # Mock the required hass attributes
    hass.config = Mock()
    hass.config.config_dir = "/test/config"
    hass.data = {DOMAIN: {mock_config_entry.entry_id: mock_coordinator}}

    result = await async_unload_entry(hass, mock_config_entry)
    assert result is True
    assert mock_config_entry.entry_id not in hass.data[DOMAIN]
