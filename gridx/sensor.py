from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .gridx_api import GridXAPI
from .entities import GridXSensor

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

    # GridX API-Client erstellen
    api = GridXAPI(
        hass,
        entry.data["username"],
        entry.data["password"],
        entry.data["client_id"],
        entry.data["realm"],
        entry.data["audience"],
    )

    # API-Authentifizierung und Gateway abrufen
    await api.authenticate()
    await api.get_gateway_id()

    # API-Daten abrufen, um Sensoren dynamisch zu erstellen
    data = await api.get_live_data()

    # Sensoren dynamisch aus der API-Response erstellen
    sensors = []
    flattened = flatten_dict(data)
    for key, _ in flattened:
        # Name aus dem Schlüssel generieren
        name = key.replace(".", " ").title()
        
        # Einheit und device_class basierend auf Schlüsselworten erraten
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
            unit = ""  # Keine Einheit für Raten
        
        # Unique ID generieren
        unique_id = f"gridx_{key.replace('.', '_')}"
        
        sensors.append(GridXSensor(api, name, unit, key, unique_id, device_class))

    async_add_entities(sensors, update_before_add=True)
