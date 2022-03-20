"""Binary sensor platform for Electrolux Status."""
from homeassistant.components.binary_sensor import BinarySensorEntity

from .entity import ElectroluxStatusEntity
from .const import BINARY_SENSOR
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    appliances = coordinator.data.get('appliances', None)

    if appliances is not None:
        for appliance_id, appliance in appliances.found_appliances.items():
            async_add_devices(
                [
                    ElectroluxBinarySensor(coordinator, entry, appliance_id, entity.entity_type, entity.attr)
                    for entity in appliance.entities if entity.entity_type == BINARY_SENSOR
                ]
            )


class ElectroluxBinarySensor(ElectroluxStatusEntity, BinarySensorEntity):
    """Electrolux Status binary_sensor class."""

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.get_entity.state
