"""Button platform for Electrolux Status."""
from homeassistant.components.button import ButtonEntity

from .entity import ElectroluxButtonEntity
from .const import BUTTON
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup button platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    appliances = coordinator.data.get('appliances', None)

    if appliances is not None:
        for appliance_id, appliance in appliances.found_appliances.items():
            async_add_devices(
                [
                    ElectroluxButton(coordinator, entry, appliance_id, entity.entity_type, entity.attr, entity.source, entity.val_to_send, entity.icon)
                    for entity in appliance.entities if entity.entity_type == BUTTON
                ]
            )


class ElectroluxButton(ElectroluxButtonEntity, ButtonEntity):
    """Electrolux Status button class."""

    async def async_press(self) -> None:
        if self.entity_attr == "ExecuteCommand":
            await self.hass.async_add_executor_job(self.coordinator.api.setHacl, self.get_appliance.pnc_id, "0x0403", self.val_to_send, self.entity_source)

