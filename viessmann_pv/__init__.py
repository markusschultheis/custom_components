from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up GridX integration from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True
