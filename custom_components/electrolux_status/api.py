import logging
import math
from typing import Union, Any

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

from .const import BINARY_SENSOR, SENSOR, BUTTON, icon_mapping
from .const import sensors, sensors_binary

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class ElectroluxLibraryEntity:
    def __init__(self, name, status, last_states, appliance_profile):
        self.name = name
        self.status: dict = status
        self.states = last_states
        self.profile = appliance_profile

    def get_name(self):
        return self.name

    def get_value(self, attr_name, field=None, source=None):
        if attr_name in ['StartTime', 'TimeToEnd', 'RunningTime', 'DryingTime', 'ApplianceTotalWorkingTime',
                         "FCTotalWashingTime"]:
            return self.time_to_end_in_minutes(attr_name, field, source)
        if attr_name in self.status:
            return self.status.get(attr_name)
        if attr_name in [self.states[k].get("name") for k in self.states]:
            val = self.get_from_states(attr_name, field, source)
            if field == "container":
                if val["1"]["name"] == "Coefficient" and val["3"]["name"] == "Exponent":
                    return val["1"]["numberValue"] * (10 ** val["3"]["numberValue"])
            else:
                return val
        if attr_name in [self.states[st]["container"][cr].get("name") for st in self.states for cr in
                         self.states[st].get("container", [])]:
            return self.get_from_states(attr_name, field, source)
        return None

    def time_to_end_in_minutes(self, attr_name, field, source):
        seconds = self.get_from_states(attr_name, field, source)
        if seconds is not None:
            if seconds == -1:
                return -1
            return int(math.ceil((int(seconds) / 60)))
        return None

    def get_from_states(self, attr_name, field, source):
        for k in self.states:
            if self.is_contained_in_states(attr_name, k, source):
                return self._get_states(self.states[k], field) if field else self._get_states(self.states[k])
            for c in self.states[k].get("container", []):
                if attr_name == self.states[k]["container"][c].get("name"):
                    return self._get_states(self.states[k]["container"][c], field) if field else self._get_states(
                        self.states[k]["container"][c])
        return None

    @staticmethod
    def _get_states(states, field=None):
        if field:
            if field in states.keys():
                return states.get(field)
            if field == "string":
                if "valueTransl" in states.keys():
                    return states.get("valueTransl").strip(" :.")
                if "valTransl" in states.keys():
                    return states.get("valTransl").strip(" :.")
                if "stringValue" in states.keys():
                    return states.get("stringValue").strip(" :.")
                return ""
        else:
            if "valueTransl" in states.keys():
                return states.get("valueTransl").strip(" :.")
            if "valTransl" in states.keys():
                return states.get("valTransl").strip(" :.")
            if "stringValue" in states.keys():
                return states.get("stringValue").strip(" :.")
            if "numberValue" in states.keys():
                return states.get("numberValue")

    def get_sensor_name(self, attr_name, source):
        for k in self.states:
            if self.is_contained_in_states(attr_name, k, source):
                return self.get_translate_name(k)
            if "container" in self.states[k]:
                return self.find_name_in_container(attr_name, k)
            return None

    def find_name_in_container(self, attr_name, k):
        for c in self.states[k].get("container", []):
            if attr_name == self.states[k]["container"][c].get("name"):
                if "nameTransl" in self.states[k]["container"][c].keys():
                    return self.states[k]["container"][c].get("nameTransl").strip(" :.")
                else:
                    return self.states[k]["container"][c].get("name").strip(" :.")
        return None

    def get_translate_name(self, k):
        if "nameTransl" in self.states[k].keys():
            return self.states[k].get("nameTransl").strip(" :.")
        else:
            return self.states[k].get("name").strip(" :.")

    def is_contained_in_states(self, attr_name, k, source):
        return attr_name == self.states[k].get("name") and source == self.states[k].get("source")

    def value_exists(self, attr_name, source):
        _container_attr = []
        for k in self.states:
            for c in self.states[k].get("container", []):
                _container_attr.append(self.states[k]["container"][c].get("name"))
        return (attr_name in self.status) or \
            (attr_name in [self.states[k].get("name") for k in self.states if
                           self.states[k].get("source") == source]) or \
            (attr_name in [self.profile[k].get("name") for k in self.profile if
                           self.profile[k].get("source") == source]) or \
            (attr_name in _container_attr)

    def sources_list(self):
        return list(
            {self.states[k].get("source") for k in self.states if self.states[k].get("source") not in ["NIU", "APL"]}
        )

    def commands_list(self, source):
        commands = list(self.profile[k].get("steps") for k in self.profile if
                        self.profile[k].get("source") == source and self.profile[k].get("name") == "ExecuteCommand")
        if len(commands) > 0:
            return commands[0]
        else:
            return {}

    def get_command_name(self, command_desc):
        if "transl" in command_desc:
            return command_desc["transl"]
        elif "key" in command_desc:
            return command_desc["key"]
        return None

    def get_suffix(self, attr_name, source):
        res = list({self.states[k].get("source") for k in self.states if self.states[k].get("name") == attr_name})
        if len(res) == 1:
            return ""
        else:
            if source in res:
                return f" ({source})"
        return ""


class ApplianceEntity:
    entity_type = None

    def __init__(self, name, attr, device_class=None, entity_category=None, field=None, source=None) -> None:
        self.attr = attr
        self.name = name
        self.device_class = device_class
        self.entity_category = entity_category
        self.field = field
        self.source = source
        self.val_to_send = None
        self.icon = None
        self._state = None

    def setup(self, data: ElectroluxLibraryEntity):
        self._state = data.get_value(self.attr, self.field, self.source)
        return self

    def clear_state(self):
        self._state = None


class ApplianceSensor(ApplianceEntity):
    entity_type = SENSOR

    def __init__(self, name, attr, unit=None, device_class=None, entity_category=None, field=None, source=None) -> None:
        super().__init__(name, attr, device_class, entity_category, field, source)
        self.unit = unit

    @property
    def state(self):
        return self._state


class ApplianceBinary(ApplianceEntity):
    entity_type = BINARY_SENSOR

    def __init__(self, name, attr, device_class=None, entity_category=None, field=None, invert=False,
                 source=None) -> None:
        super().__init__(name, attr, device_class, entity_category, field, source)
        self.invert = invert

    @property
    def state(self):
        state = self._state in [1, 'enabled', True, 'Connected', 'connect']
        return not state if self.invert else state


class ApplianceButton(ApplianceEntity):
    entity_type = BUTTON

    def __init__(self, name, attr, unit=None, device_class=None, entity_category=None, source=None, val_to_send=None,
                 icon=None) -> None:
        super().__init__(name, attr, device_class, entity_category, None, source)
        self.val_to_send = val_to_send
        self.icon = icon

    def setup(self, data: ElectroluxLibraryEntity):
        return self


class Appliance:
    brand: str
    device: str
    entities: []

    def __init__(self, name, pnc_id, brand, model) -> None:
        self.model = model
        self.pnc_id = pnc_id
        self.name = name
        self.brand = brand

    def get_entity(self, entity_type, entity_attr, entity_source, val_to_send):
        return next(
            entity
            for entity in self.entities
            if
            entity.attr == entity_attr and entity.entity_type == entity_type and entity.source == entity_source and entity.val_to_send == val_to_send
        )

    def setup(self, data: ElectroluxLibraryEntity):
        entities = [
            ApplianceBinary(
                name=data.get_name(),
                attr='status',
                device_class=BinarySensorDeviceClass.CONNECTIVITY,
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
                name=f"{data.get_name()} {data.get_sensor_name('LinkQualityIndicator', 'NIU')}",
                attr='LinkQualityIndicator',
                field='numberValue',
                entity_category=EntityCategory.DIAGNOSTIC,
                source='NIU',
            ),
        ]
        sources = data.sources_list()
        for src in sources:
            for sensor_type, sensors_list in sensors.items():
                for sensor_name, params in sensors_list.items():
                    entities.append(
                        ApplianceSensor(
                            name=f"{data.get_name()} {data.get_sensor_name(sensor_name, src)}{data.get_suffix(sensor_name, src)}",
                            attr=sensor_name,
                            field=params[0],
                            device_class=params[1],
                            entity_category=sensor_type,
                            unit=params[2],
                            source=src,
                        )
                    )
            for sensor_type, sensors_list in sensors_binary.items():
                for sensor_name, params in sensors_list.items():
                    entities.append(
                        ApplianceBinary(
                            name=f"{data.get_name()} {data.get_sensor_name(sensor_name, src)}{data.get_suffix(sensor_name, src)}",
                            attr=sensor_name,
                            field=params[0],
                            device_class=params[1],
                            entity_category=sensor_type,
                            invert=params[2],
                            source=src,
                        )
                    )
            for key, command in data.commands_list(src).items():
                entities.append(
                    ApplianceButton(
                        name=f"{data.get_name()} {data.get_command_name(command)}{data.get_suffix('ExecuteCommand', src)}",
                        attr='ExecuteCommand',
                        val_to_send=key,
                        source=src,
                        icon=icon_mapping.get(key, "mdi:gesture-tap-button"),
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
