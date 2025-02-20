import requests
import logging
import time
from influxdb import InfluxDBClient
from homeassistant.helpers.entity import Entity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType
from .const import DOMAIN, GRIDX_URLS, GRIDX_LOGIN, INFLUX_HOST, INFLUX_PORT, INFLUX_DATABASE, DEFAULT_UPDATE_INTERVAL, LOGGER_NAME

_LOGGER = logging.getLogger(LOGGER_NAME)


class GridXSensor(Entity):
    """Sensor for retrieving GridX PV data and storing it in InfluxDB."""

    def __init__(self, hass, name, username, password):
        """Initialize the sensor."""
        self.hass = hass
        self._name = name
        self._state = None
        self._username = username
        self._password = password
        self._token = None
        self._token_expiry = 0  # Timestamp when the token expires
        self._gateway_id = None
        self._last_update = 0
        self.client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT, database=INFLUX_DATABASE)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    def update(self):
        """Regularly fetch live data and store it in InfluxDB."""
        now = time.time()

        # Check if token is expired or close to expiry
        if not self._token or now >= self._token_expiry:
            self._refresh_access_token()

        if self._token:
            data = self._fetch_live_data()
            if data:
                self._state = data["power"]  # Set current power as entity state
                self._store_in_influxdb(data)
        else:
            _LOGGER.error("Failed to retrieve valid access token.")

    def _refresh_access_token(self):
        """Refreshes the OAuth access token."""
        auth_data = GRIDX_LOGIN.copy()
        auth_data["username"] = self._username
        auth_data["password"] = self._password

        response = requests.post(GRIDX_URLS["login"], json=auth_data)

        if response.status_code == 200:
            token_data = response.json()
            self._token = token_data.get("access_token")
            expires_in = token_data.get("expires_in", 3600)  # Default to 1 hour
            self._token_expiry = time.time() + expires_in - 60  # Refresh 1 min before expiry
            _LOGGER.info("Successfully refreshed access token.")
        else:
            _LOGGER.error("OAuth login failed: %s", response.text)
            self._token = None

    def _get_gateway_id(self):
        """Retrieves the GridX gateway ID."""
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(GRIDX_URLS["gateways"], headers=headers)

        if response.status_code == 200:
            gateways = response.json()
            if gateways:
                return gateways[0].get("system", {}).get("id")
        _LOGGER.error("Failed to retrieve gateway ID")
        return None

    def _fetch_live_data(self):
        """Fetches live PV data from GridX."""
        if not self._gateway_id:
            self._gateway_id = self._get_gateway_id()

        if not self._gateway_id:
            return None

        url = GRIDX_URLS["live"].format(self._gateway_id)
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(url, headers=headers)

        # Handle token expiration
        if response.status_code == 401:
            _LOGGER.warning("Access token expired, refreshing...")
            self._refresh_access_token()
            headers["Authorization"] = f"Bearer {self._token}"
            response = requests.get(url, headers=headers)  # Retry with new token

        if response.status_code == 200:
            return response.json()
        else:
            _LOGGER.error("Failed to retrieve live data: %s", response.text)
            return None

    def _store_in_influxdb(self, data):
        """Stores the retrieved values in InfluxDB."""
        measurement = "HA_PV_Monitoring"
        fields = {
            "power": int(data["batteries"][0]["power"]),
            "remainingCharge": int(data["batteries"][0]["remainingCharge"]),
            "stateOfCharge": float(data["batteries"][0]["stateOfCharge"]),
            "consumption": int(data["consumption"]),
            "directConsumption": int(data["directConsumption"]),
            "directConsumptionHousehold": int(data["directConsumptionHousehold"]),
            "directConsumptionRate": int(data["directConsumptionRate"]),
            "grid": int(data["grid"]),
            "measuredAt": data["measuredAt"],
            "photovoltaic": int(data["photovoltaic"]),
            "production": int(data["production"]),
            "selfConsumption": int(data["selfConsumption"]),
            "selfConsumptionRate": int(data["selfConsumptionRate"]),
            "selfSufficiencyRate": float(data["selfSufficiencyRate"]),
            "selfSupply": int(data["selfSupply"]),
            "totalConsumption": int(data["totalConsumption"])
        }

        data_point = [
            {
                "measurement": measurement,
                "time": data["measuredAt"],
                "fields": fields
            }
        ]

        try:
            self.client.write_points(data_point)
            _LOGGER.info("Successfully stored data in InfluxDB")
        except Exception as e:
            _LOGGER.error("Error storing data in InfluxDB: %s", str(e))


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up the integration in Home Assistant."""
    sensor = GridXSensor(hass, "GridX PV Sensor", entry.data["username"], entry.data["password"])
    hass.data.setdefault(DOMAIN, {})["sensor"] = sensor

    async def handle_update(call):
        """Handler for manual data update."""
        _LOGGER.info("Manually triggered GridX data fetch")
        sensor.update()

    hass.services.async_register(DOMAIN, "update_data", handle_update)

    return True
