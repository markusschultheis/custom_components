"""Calculated sensor entities for GridX integration."""
import logging
from typing import Any, Optional
from homeassistant.components.sensor import SensorEntity, SensorStateClass, SensorDeviceClass
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .helpers import extract_nested_value, safe_divide

_LOGGER = logging.getLogger(__name__)


class GridXCalculatedSensor(CoordinatorEntity, SensorEntity):
    """Base class for calculated GridX sensors."""

    def __init__(
        self,
        coordinator: Any,
        name: str,
        unique_id: str,
        unit: Optional[str],
        device_class: Optional[str] = None,
        state_class: Optional[SensorStateClass] = None,
    ) -> None:
        """Initialize the calculated sensor."""
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class or SensorStateClass.MEASUREMENT
        
        # Set device info to group with other GridX sensors
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.api.gateway_id)},
            name="GridX System",
            manufacturer="GridX",
            model="GridX Gateway",
        )

    @property
    def available(self) -> bool:
        """Return if the sensor is available."""
        return self.coordinator.last_update_success


class BatteryChargePowerSensor(GridXCalculatedSensor):
    """Sensor for battery charging power (positive when charging)."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize the battery charge power sensor."""
        super().__init__(
            coordinator=coordinator,
            name="GridX Battery Charge Power",
            unique_id="gridx_battery_charge_power",
            unit="W",
            device_class=SensorDeviceClass.POWER,
        )

    @property
    def native_value(self) -> Optional[float]:
        """Return battery power (positive = charging, negative = discharging)."""
        if self.coordinator.data is None:
            return None
        
        battery_power = extract_nested_value(self.coordinator.data, "battery.power")
        return battery_power


class BatteryEnergyStoredSensor(GridXCalculatedSensor):
    """Sensor for actual energy stored in battery (capacity * state of charge)."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize the battery energy stored sensor."""
        super().__init__(
            coordinator=coordinator,
            name="GridX Battery Energy Stored",
            unique_id="gridx_battery_energy_stored",
            unit="Wh",
            device_class=SensorDeviceClass.ENERGY,
        )

    @property
    def native_value(self) -> Optional[float]:
        """Calculate actual energy stored in battery."""
        if self.coordinator.data is None:
            return None
        
        # Use remainingCharge if available, otherwise calculate from capacity and SOC
        remaining_charge = extract_nested_value(self.coordinator.data, "battery.remainingCharge")
        if remaining_charge is not None:
            return remaining_charge
        
        capacity = extract_nested_value(self.coordinator.data, "battery.capacity")
        soc = extract_nested_value(self.coordinator.data, "battery.stateOfCharge")
        
        if capacity is None or soc is None:
            return None
        
        try:
            return (capacity * soc) / 100
        except (TypeError, ValueError, ZeroDivisionError):
            return None


class GridExportRateSensor(GridXCalculatedSensor):
    """Sensor for grid export rate (production / consumption ratio)."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize the grid export rate sensor."""
        super().__init__(
            coordinator=coordinator,
            name="GridX Grid Export Rate",
            unique_id="gridx_grid_export_rate",
            unit="%",
        )

    @property
    def native_value(self) -> Optional[float]:
        """Calculate what percentage of production is exported to grid."""
        if self.coordinator.data is None:
            return None
        
        production = extract_nested_value(self.coordinator.data, "production")
        self_consumption = extract_nested_value(self.coordinator.data, "selfConsumption")
        
        if production is None or self_consumption is None:
            return None
        
        if production == 0:
            return 0.0
        
        try:
            grid_export = production - self_consumption
            return (grid_export / production) * 100
        except (TypeError, ValueError, ZeroDivisionError):
            return None


class HouseholdConsumptionRateSensor(GridXCalculatedSensor):
    """Sensor for household consumption as percentage of total consumption."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize the household consumption rate sensor."""
        super().__init__(
            coordinator=coordinator,
            name="GridX Household Consumption Rate",
            unique_id="gridx_household_consumption_rate",
            unit="%",
        )

    @property
    def native_value(self) -> Optional[float]:
        """Calculate household consumption percentage."""
        if self.coordinator.data is None:
            return None
        
        household = extract_nested_value(self.coordinator.data, "directConsumptionHousehold")
        total_consumption = extract_nested_value(self.coordinator.data, "totalConsumption")
        
        if household is None or total_consumption is None or total_consumption == 0:
            return None
        
        return safe_divide(household, total_consumption, 0.0) * 100


class SolarCoverageRateSensor(GridXCalculatedSensor):
    """Sensor for how much of consumption is covered by solar (real-time)."""

    def __init__(self, coordinator: Any) -> None:
        """Initialize the solar coverage rate sensor."""
        super().__init__(
            coordinator=coordinator,
            name="GridX Solar Coverage Rate",
            unique_id="gridx_solar_coverage_rate",
            unit="%",
        )

    @property
    def native_value(self) -> Optional[float]:
        """Calculate what percentage of consumption is covered by solar."""
        if self.coordinator.data is None:
            return None
        
        direct_consumption = extract_nested_value(self.coordinator.data, "directConsumption")
        total_consumption = extract_nested_value(self.coordinator.data, "totalConsumption")
        
        if direct_consumption is None or total_consumption is None or total_consumption == 0:
            return None
        
        return safe_divide(direct_consumption, total_consumption, 0.0) * 100


# List of all calculated sensor classes
CALCULATED_SENSOR_CLASSES = [
    BatteryChargePowerSensor,
    BatteryEnergyStoredSensor,
    GridExportRateSensor,
    HouseholdConsumptionRateSensor,
    SolarCoverageRateSensor,
]
