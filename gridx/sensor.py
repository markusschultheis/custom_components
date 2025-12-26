from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import logging
from .gridx_api import GridXAPI
from .entities import GridXSensor

_LOGGER = logging.getLogger(__name__)

def flatten_dict(d, prefix=''):
    """Flatten a nested dict into a list of (key_path, value) tuples for numeric values."""
    items = []
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key))
        elif isinstance(v, list):
            # Handle lists: if list of dicts, take the first item; if list of numbers, skip for now
            if v and isinstance(v[0], dict):
                items.extend(flatten_dict(v[0], f"{new_key}.0"))
        elif isinstance(v, (int, float)):
            items.append((new_key, v))
    return items

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up GridX sensors from a config entry."""
    try:
        # Create GridX API client
        api = GridXAPI(
            hass,
            entry.data["username"],
            entry.data["password"],
            entry.data["client_id"],
            entry.data["realm"],
            entry.data["audience"],
        )

        # Authenticate and retrieve gateway
        await api.authenticate()
        await api.get_gateway_id()

        # Retrieve API data to create sensors dynamically
        data = await api.get_live_data()

        # Create sensors dynamically from API response
        sensors = []
        flattened = flatten_dict(data)
        for key, _ in flattened:
            # Generate name from key
            name = key.replace(".", " ").title()
            
            # Determine unit and device_class based on keywords
            unit = None
            device_class = None
            key_lower = key.lower()
            if "power" in key_lower:
                unit = "W"
                device_class = "power"
            elif any(word in key_lower for word in ["charge", "capacity", "production", "consumption", "supply", "grid", "photovoltaic", "directconsumption"]):
                unit = "Wh"
                device_class = "energy"
            elif "stateofcharge" in key_lower:
                unit = "%"
            elif "rate" in key_lower:
                unit = ""  # No unit for rates
            
            # Generate unique ID
            unique_id = f"gridx_{key.replace('.', '_')}"
            
            sensors.append(GridXSensor(api, name, unit, key, unique_id, device_class))

        async_add_entities(sensors, update_before_add=True)
    except Exception as err:
        _LOGGER.error("Failed to setup GridX sensors: %s", err)
        raise
