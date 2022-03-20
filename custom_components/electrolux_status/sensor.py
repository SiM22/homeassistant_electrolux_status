from typing import cast

from .api import ApplianceSensor
from .const import DOMAIN
from .const import SENSOR
from .entity import ElectroluxStatusEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    appliances = coordinator.data.get('appliances', None)

    if appliances is not None:
        for appliance_id, appliance in appliances.found_appliances.items():
            async_add_devices(
                [
                    ElectroluxStatusSensor(coordinator, entry, appliance_id, entity.entity_type, entity.attr)
                    for entity in appliance.entities if entity.entity_type == SENSOR
                ]
            )


class ElectroluxStatusSensor(ElectroluxStatusEntity):
    """Electrolux Status Sensor class."""

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.get_entity.state

    @property
    def unit_of_measurement(self):
        return cast(ApplianceSensor, self.get_entity).unit
