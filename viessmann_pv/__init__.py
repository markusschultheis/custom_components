from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform

from .const import DOMAIN, DATA_ACCESS_TOKEN, DATA_REFRESH_TOKEN, DATA_EXPIRES_AT, DATA_ID_TOKEN

PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up GridX integration from a config entry."""

    # Initialisiere den Speicher
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN].setdefault(DATA_ACCESS_TOKEN, None)
    hass.data[DOMAIN].setdefault(DATA_REFRESH_TOKEN, None)
    hass.data[DOMAIN].setdefault(DATA_EXPIRES_AT, 0)
    hass.data[DOMAIN].setdefault(DATA_ID_TOKEN, None)

    # Sensor-Setup weiterleiten
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(DOMAIN, None)
    return unload_ok
