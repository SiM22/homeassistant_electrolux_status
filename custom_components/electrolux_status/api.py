import logging
import math

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_CONNECTIVITY,
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_LOCK,
)
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

from .const import BINARY_SENSOR, SENSOR
from homeassistant.const import TIME_MINUTES

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class ElectroluxLibraryEntity:
    def __init__(self, name, status, profiles):
        self.name = name
        self.status: dict = status
        self.profiles = profiles

    def get_name(self):
        return self.name

    def get_value(self, attr_name, field=None, source=None):
        if attr_name == 'TimeToEnd':
            return self.time_to_end_in_minutes(attr_name, field, source)
        if attr_name in self.status:
            return self.status.get(attr_name)
        if attr_name in [self.profiles[k].get("name") for k in self.profiles]:
            return self.get_from_profiles(attr_name, field, source)
        return None

    def time_to_end_in_minutes(self, attr_name, field, source):
        seconds = self.get_from_profiles(attr_name, field, source)
        if seconds is not None:
            if seconds == -1:
                return -1
            return int(math.ceil((seconds / 60)))
        return None

    def get_from_profiles(self, attr_name, field, source):
        for k in self.profiles:
            if attr_name == self.profiles[k].get("name") and source == self.profiles[k].get("source"):
                if field and field in self.profiles[k].keys():
                    return self.profiles[k].get(field)
                if "stringValue" in self.profiles[k].keys():
                    return self.profiles[k].get("stringValue")
                if "numberValue" in self.profiles[k].keys():
                    return self.profiles[k].get("numberValue")
        return None

    def value_exists(self, attr_name, source):
        return (attr_name in self.status) or (attr_name in [self.profiles[k].get("name") for k in self.profiles if self.profiles[k].get("source") == source])

    def sources_list(self):
        res = list({self.profiles[k].get("source") for k in self.profiles if self.profiles[k].get("source") not in ["NIU", "APL"]})
        return res


class ApplianceEntity:
    entity_type = None

    def __init__(self, name, attr, device_class=None, entity_category=None, field=None, source=None) -> None:
        self.attr = attr
        self.name = name
        self.device_class = device_class
        self.entity_category = entity_category
        self.field = field
        self.source = source
        self._state = None

    def setup(self, data: ElectroluxLibraryEntity):
        self._state = data.get_value(self.attr, self.field, self.source)
        return self

    def clear_state(self):
        self._state = None

    @property
    def state(self):
        return self._state


class ApplianceSensor(ApplianceEntity):
    entity_type = SENSOR

    def __init__(self, name, attr, unit=None, device_class=None, entity_category=None, field=None, source=None) -> None:
        super().__init__(name, attr, device_class, entity_category, field, source)
        self.unit = unit


class ApplianceBinary(ApplianceEntity):
    entity_type = BINARY_SENSOR

    def __init__(self, name, attr, device_class=None, entity_category=None, field=None, invert=False, source=None) -> None:
        super().__init__(name, attr, device_class, entity_category, field, source)
        self.invert = invert

    @property
    def state(self):
        state = self._state in [1, 'enabled', True, 'Connected', 'connect']
        return not state if self.invert else state


class Appliance:
    brand: str
    device: str
    entities: []

    def __init__(self, name, pnc_id, brand, model) -> None:
        self.model = model
        self.pnc_id = pnc_id
        self.name = name
        self.brand = brand

    def get_entity(self, entity_type, entity_attr, entity_source):
        return next(
            entity
            for entity in self.entities
            if entity.attr == entity_attr and entity.entity_type == entity_type and entity.source == entity_source
        )

    def setup(self, data: ElectroluxLibraryEntity):
        entities = [
            ApplianceBinary(
                name=data.get_name(),
                attr='status',
                device_class=DEVICE_CLASS_CONNECTIVITY,
                entity_category=EntityCategory.DIAGNOSTIC,
                source='APL',
            ),
            ApplianceSensor(
                name=f"{data.get_name()} SSID",
                attr='Ssid',
                entity_category=EntityCategory.DIAGNOSTIC,
                source='NIU',
            ),
            ApplianceSensor(
                name=f"{data.get_name()} Signal Strength",
                attr='LinkQualityIndicator',
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                entity_category=EntityCategory.DIAGNOSTIC,
                source='NIU',
            ),
        ]
        sources = data.sources_list()
        for src in sources:
            if len(sources) > 1:
                suffix = f" ({src})"
            else:
                suffix = ""
            entities.append(
                ApplianceBinary(
                    name=f"{data.get_name()} Door{suffix}",
                    attr='DoorState', field='numberValue',
                    device_class=DEVICE_CLASS_DOOR,
                    source=src,
                )
            )
            entities.append(
                ApplianceBinary(
                    name=f"{data.get_name()} Door Lock{suffix}",
                    attr='DoorLock', field='numberValue',
                    device_class=DEVICE_CLASS_LOCK,
                    invert=True,
                    source=src,
                )
            )
            entities.append(
                ApplianceSensor(
                    name=f"{data.get_name()} Time To End{suffix}",
                    attr='TimeToEnd',
                    unit=TIME_MINUTES,
                    source=src,
                )
            )
            entities.append(
                ApplianceSensor(
                    name=f"{data.get_name()} Cycle Phase{suffix}",
                    attr='CyclePhase',
                    source=src,
                )
            )

        self.entities = [
            entity.setup(data)
            for entity in entities if data.value_exists(entity.attr, entity.source)
        ]


class Appliances:
    def __init__(self, found_appliances) -> None:
        self.found_appliances = found_appliances

    def get_appliance(self, pnc_id):
        return self.found_appliances.get(pnc_id, None)
