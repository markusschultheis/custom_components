from homeassistant.components.sensor import SensorEntity

class ViessmannSensor(SensorEntity):
    def __init__(self, api, name, key):
        self.api = api
        self._name = name
        self._key = key
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update(self):
        data = await self.api.get_live_data()
        self._state = data.get(self._key)
