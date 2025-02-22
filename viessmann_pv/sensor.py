from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .gridx_api import GridXAPI
from .entities import ViessmannSensor 

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up GridX sensors from a config entry."""
    
    # GridX API-Client erstellen
    api = GridXAPI(
        entry.data["username"],
        entry.data["password"],
        entry.data["client_id"],
        entry.data["realm"],
        entry.data["audience"],
    )

    # API-Authentifizierung und Gateway abrufen
    await api.authenticate()
    await api.get_gateway_id()

    # Sensoren erstellen
    sensors = [
        ViessmannSensor(api, "PV Power", "photovoltaic"),
        ViessmannSensor(api, "Grid Power", "grid"),
        ViessmannSensor(api, "Battery Charge", "stateOfCharge"),
        ViessmannSensor(api, "Remaining Charge", "remainingCharge"),
        ViessmannSensor(api, "Direct Consumption", "directConsumption"),
        ViessmannSensor(api, "Consumption", "consumption"),
        ViessmannSensor(api, "Total Consumption", "totalConsumption"),
        ViessmannSensor(api, "Production", "production"),
        ViessmannSensor(api, "Self Supply", "selfSupply"),
        ViessmannSensor(api, "Self Suffieciency Rate", "selfSufficiencyRate"),
        ViessmannSensor(api, "Grid Meter Reading Positiv", "gridMeterReadingPositive"),
        ViessmannSensor(api, "Grid Meter Reading Negativ", "gridMeterReadingNegative")
    ]
    
    async_add_entities(sensors, update_before_add=True)
