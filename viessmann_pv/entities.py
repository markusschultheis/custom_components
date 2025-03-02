rom homeassistant.components.sensor import SensorEntity

class ViessmannSensor(SensorEntity):
    def __init__(self, api, name, unit, key, unique_id, device_class):
        self.api = api
        self._name = name
        self._key = key
        self._state = None
        self._unit = unit
        self._unique_id = unique_id
        self._device_class = device_class
        self._state_class = "total"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def device_class(self):
        return self._device_class

    async def async_update(self):
        """Daten nur aktualisieren, nicht neu anlegen."""
        data = await self.api.get_live_data()
        self._state = self.extract_value(data)

    def extract_value(self, data):
        """Extrahiert den gewünschten Wert aus der API-Antwort."""
        keys = self._key.split(".")
        value = data
        for key in keys:
            value = value.get(key, None)
            if value is None:
                return None
        return value
