from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN


class GridXSensor(SensorEntity):
    """Representation of a GridX sensor."""

    def __init__(self, api, name, unit, key, unique_id, device_class):
        """Initialize the sensor."""
        self.api = api
        self._name = name
        self._key = key
        self._state = None
        self._unit = unit
        self._unique_id = unique_id
        self._device_class = device_class
        self._state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.api.gateway_id)},
            name="GridX System",
            manufacturer="GridX",
            model="GridX Gateway",
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return self._unique_id

    @property
    def device_class(self):
        """Return the device class."""
        return self._device_class

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.api.gateway_id)},
            name="GridX System",
            manufacturer="GridX",
            model="GridX Gateway",
        )

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        return self.api.gateway_id is not None

    async def async_update(self):
        """Update sensor data."""
        data = await self.api.get_live_data()
        self._state = self.extract_value(data)

    def extract_value(self, data):
        """Extract the desired value from the API response."""
        keys = self._key.split(".")
        value = data
        for key in keys:
            value = value.get(key, None)
            if value is None:
                return None
        return value
