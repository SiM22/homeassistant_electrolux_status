import logging

from homeassistant.components.binary_sensor import DEVICE_CLASS_CONNECTIVITY

from .const import BINARY_SENSOR, SENSOR
from homeassistant.const import TIME_SECONDS
_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class ElectroluxLibraryEntity:
    def __init__(self, name, status, profiles):
        self.name = name
        self.status: dict = status
        self.profiles = profiles

    def get_name(self):
        return self.name

    def get_value(self, attr_name):
        if attr_name in self.status:
            return self.status.get(attr_name)
        if attr_name in [self.profiles[k].get("name") for k in self.profiles]:
            for k in self.profiles:
                if attr_name == self.profiles[k].get("name"):
                    if "stringValue" in self.profiles[k].keys():
                        return self.profiles[k].get("stringValue")
                    if "numberValue" in self.profiles[k].keys():
                        return self.profiles[k].get("numberValue")
        return None

    def value_exists(self, attr_name):
        return (attr_name in self.status) or (attr_name in [self.profiles[k].get("name") for k in self.profiles])


class ApplianceEntity:
    entity_type: int = None

    def __init__(self, name, attr, device_class=None) -> None:
        self.attr = attr
        self.name = name
        self.device_class = device_class
        self._state = None

    def setup(self, data: ElectroluxLibraryEntity):
        self._state = data.get_value(self.attr)
        return self

    def clear_state(self):
        self._state = None

    @property
    def state(self):
        return self._state


class ApplianceSensor(ApplianceEntity):
    entity_type: int = SENSOR

    def __init__(self, name, attr, unit="", device_class=None) -> None:
        super().__init__(name, attr, device_class)
        self.unit = unit


class ApplianceBinary(ApplianceEntity):
    entity_type: int = BINARY_SENSOR

    def __init__(self, name, attr, device_class=None) -> None:
        super().__init__(name, attr, device_class)

    @property
    def state(self):
        return self._state in ['enabled', True, 'Connected', 'connect']


class Appliance:
    serialNumber: str
    brand: str
    device: str
    entities: []

    def __init__(self, name, pnc_id, brand, model) -> None:
        self.model = model
        self.pnc_id = pnc_id
        self.name = name
        self.brand = brand

    def get_entity(self, entity_type, entity_attr):
        return next(
            entity
            for entity in self.entities
            if entity.attr == entity_attr and entity.entity_type == entity_type
        )

    def setup(self, data: ElectroluxLibraryEntity):
        dryer_entities = [
            ApplianceBinary(
                name=data.get_name(),
                attr='status',
                device_class=DEVICE_CLASS_CONNECTIVITY
            ),
            ApplianceSensor(
                name=f"{data.get_name()} Time To End",
                attr='TimeToEnd',
                unit=TIME_SECONDS,
            ),
            ApplianceSensor(
                name=f"{data.get_name()} Cycle Phase",
                attr='CyclePhase'
            )
        ]
        self.entities = [
            entity.setup(data)
            for entity in dryer_entities if data.value_exists(entity.attr)
        ]


class Appliances:
    def __init__(self, appliances) -> None:
        self.appliances = appliances

    def get_appliance(self, pnc_id):
        return self.appliances.get(pnc_id, None)
