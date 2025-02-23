rom homeassistant.core import HomeAssistant
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
        ViessmannSensor(api, "PV Power", "Wh", "photovoltaic", "Viessmann_photovolatic", "energy"),
        ViessmannSensor(api, "Grid Power", "Wh", "grid", "Viessmann_grid", "energie"),
        ViessmannSensor(api, "State of Charge", "%", "battery.stateOfCharge", "Viessmann_stateOfCharge", ""),
        ViessmannSensor(api, "Remaining Charge", "Wh", "battery.remainingCharge", "Viessmann_remainingCharge", ""),
        ViessmannSensor(api, "Consumption", "Wh", "consumption", "Viessmann_consumption", "energy"),
        ViessmannSensor(api, "Direct Consumption", "Wh", "directConsumption", "Viessmann_directConsumption", "energy"),
        ViessmannSensor(api, "Direct Consumption household", "Wh", "directConsumptionHousehold", "Viessmann_HhConsumption", "energy"),
        ViessmannSensor(api, "Total Consumption", "W", "totalConsumption", "Viessmann_totalConsumption", "energy"),
        ViessmannSensor(api, "Production", "Wh", "production", "Viessmann_production", "energy"),
        ViessmannSensor(api, "Self Supply", "Wh", "selfSupply", "Viessmann_selfSupply", "energy"),
        ViessmannSensor(api, "Self Suffieciency Rate", "", "selfSufficiencyRate", "Viessmann_selfSufficencyRate", ""),
        ViessmannSensor(api, "Grid Meter Reading Positiv", "Wh", "gridMeterReadingPositive", "Viessmann_gridMeterPos", ""),
        ViessmannSensor(api, "Grid Meter Reading Negativ", "Wh", "gridMeterReadingNegative", "Viessmann_gridMeterNeg", "")
    ]

    async_add_entities(sensors, update_before_add=True)
