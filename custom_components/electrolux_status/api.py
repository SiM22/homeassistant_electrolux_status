import logging
import math
import re

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from pyelectroluxocp.apiModels import ApplianceInfoResponse, ApplienceStatusResponse

from .const import BINARY_SENSOR, SENSOR, BUTTON, icon_mapping
from .const import sensors, sensors_binary

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class ElectroluxLibraryEntity:
    def __init__(self, name, status: str, state: ApplienceStatusResponse, appliance_info: ApplianceInfoResponse,
                 capabilities: dict[str, any]):
        self.name = name
        self.status = status
        self.state = state
        self.reported_state = self.state["properties"]["reported"]
        self.appliance_info = appliance_info
        self.capabilities = capabilities

    def get_name(self):
        return self.name

    def get_value(self, attr_name, field=None, source=None):
        if source and source != '':
            entry = self.reported_state[source][attr_name]
        else:
            entry = self.reported_state[attr_name]
        return entry
        # if attr_name in ["TargetMicrowavePower"]:
        #     return self.fix_microwave_power(attr_name, field, source)
        # if attr_name in ["LinkQualityIndicator"]:
        #     return self.num_to_dbm(attr_name, field, source)
        # if attr_name in ['StartTime', 'TimeToEnd', 'RunningTime', 'DryingTime', 'ApplianceTotalWorkingTime',
        #                  "FCTotalWashingTime"]:
        #     return self.time_to_end_in_minutes(attr_name, field, source)
        # if attr_name in self.status:
        #     return self.status.get(attr_name)
        # if attr_name in [self.state[k].get("name") for k in self.state]:
        #     val = self.get_from_states(attr_name, field, source)
        #     if field == "container":
        #         if val["1"]["name"] == "Coefficient" and val["3"]["name"] == "Exponent":
        #             return val["1"]["numberValue"] * (10 ** val["3"]["numberValue"])
        #     else:
        #         return val
        # if attr_name in [self.state[st]["container"][cr].get("name") for st in self.state for cr in
        #                  self.state[st].get("container", [])]:
        #     return self.get_from_states(attr_name, field, source)
        # return None

    # def time_to_end_in_minutes(self, attr_name, field, source):
    #     seconds = self.get_from_states(attr_name, field, source)
    #     if seconds is not None:
    #         if seconds == -1:
    #             return -1
    #         return int(math.ceil((int(seconds) / 60)))
    #     return None
    #
    # def fix_microwave_power(self, attr_name, field, source):
    #     microwave_power = self.get_from_states(attr_name, field, source)
    #     if microwave_power is not None:
    #         if microwave_power == 65535:
    #             return 0
    #         return microwave_power
    #     return None
    #
    # def num_to_dbm(self, attr_name, field, source):
    #     number_from_0_to_5 = self.get_from_states(attr_name, field, source)
    #     if number_from_0_to_5 is not None:
    #         if int(number_from_0_to_5) == 0:
    #             return -110
    #         if int(number_from_0_to_5) == 1:
    #             return -80
    #         if int(number_from_0_to_5) == 2:
    #             return -70
    #         if int(number_from_0_to_5) == 3:
    #             return -60
    #         if int(number_from_0_to_5) == 4:
    #             return -55
    #         if int(number_from_0_to_5) == 5:
    #             return -20
    #     return None

    # def get_from_states(self, attr_name, field, source):
    #     for k in self.state:
    #         if attr_name == self.state[k].get("name") and source == self.state[k].get("source"):
    #             return self._get_states(self.state[k], field) if field else self._get_states(self.state[k])
    #         attr_val = None
    #         for c in self.state[k].get("container", []):
    #             if attr_name == self.state[k]["container"][c].get("name"):
    #                 attr_val = self._get_states(self.state[k]["container"][c], field) if field else self._get_states(
    #                     self.state[k]["container"][c])
    #         if attr_val is not None:
    #             return attr_val
    #     return None

    # @staticmethod
    # def _get_states(states, field=None):
    #     if field:
    #         if field in states.keys():
    #             return states.get(field)
    #         if field == "string":
    #             if "valueTransl" in states.keys():
    #                 return states.get("valueTransl").strip(" :.")
    #             if "valTransl" in states.keys():
    #                 return states.get("valTransl").strip(" :.")
    #             if "stringValue" in states.keys():
    #                 return states.get("stringValue").strip(" :.")
    #             return ""
    #     else:
    #         if "valueTransl" in states.keys():
    #             return states.get("valueTransl").strip(" :.")
    #         if "valTransl" in states.keys():
    #             return states.get("valTransl").strip(" :.")
    #         if "stringValue" in states.keys():
    #             return states.get("stringValue").strip(" :.")
    #         if "numberValue" in states.keys():
    #             return states.get("numberValue")

    def get_sensor_name(self, attr_name: str, container: str = None):
        # Convert format "fCMiscellaneousState/detergentExtradosage" to "Detergent extradosage"
        attr_name = attr_name.rpartition('/')[-1] or attr_name
        attr_name = attr_name[0].upper() + attr_name[1:]
        attr_name = " ".join(re.findall('[A-Z][^A-Z]*', attr_name))
        attr_name = attr_name.capitalize()
        return attr_name

    def get_category(self, attr_name: str):
        # Extract category ex: "fCMiscellaneousState/detergentExtradosage" to "fCMiscellaneousState"
        # or "" if none
        return attr_name.rpartition('/')[0]

    # def value_exists(self, attr_name, source):
    #     _container_attr = []
    #     for k in self.state:
    #         for c in self.state[k].get("container", []):
    #             _container_attr.append(self.state[k]["container"][c].get("name"))
    #     return (attr_name in self.status) or \
    #         (attr_name in [self.state[k].get("name") for k in self.state if
    #                        self.state[k].get("source") == source]) or \
    #         (attr_name in [self.profile[k].get("name") for k in self.profile if
    #                        self.profile[k].get("source") == source]) or \
    #         (attr_name in _container_attr)

    def sources_list(self):
        return filter(lambda key: not key.startswith("applianceCareAndMaintenance"),list(self.capabilities.keys()))
        # return list(
        #     {self.state[k].get("source") for k in self.state if self.state[k].get("source") not in ["NIU", "APL"]}
        # )

    # def commands_list(self, source):
    #     commands = list(self.profile[k].get("steps") for k in self.profile if
    #                     self.profile[k].get("source") == source and self.profile[k].get("name") == "ExecuteCommand")
    #     if len(commands) > 0:
    #         return commands[0]
    #     else:
    #         return {}

    # def get_command_name(self, command_desc):
    #     if "transl" in command_desc:
    #         return command_desc["transl"]
    #     elif "key" in command_desc:
    #         return command_desc["key"]
    #     return None


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
        # TODO
        # entities = [
        #     ApplianceBinary(
        #         name=data.get_name(),
        #         attr='status',
        #         device_class=BinarySensorDeviceClass.CONNECTIVITY,
        #         entity_category=EntityCategory.DIAGNOSTIC,
        #         source='APL',
        #     ),
        #     ApplianceSensor(
        #         name=f"{data.get_name()} SSID",
        #         attr='Ssid',
        #         entity_category=EntityCategory.DIAGNOSTIC,
        #         source='NIU',
        #     ),
        #     ApplianceSensor(
        #         name=f"{data.get_name()} {data.get_sensor_name('LinkQualityIndicator', 'NIU')}",
        #         attr='LinkQualityIndicator',
        #         field='numberValue',
        #         device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        #         unit="dBm",
        #         entity_category=EntityCategory.DIAGNOSTIC,
        #         source='NIU',
        #     ),
        # ]

        entities = []
        # Extraction of the capabilities of the connected appliance and mapping to the known entities of the component
        sources = data.sources_list() # [ "applianceState", "autoDosing",..., "userSelections/analogTemperature",...]

        # For each capability src
        for src in sources:
            category = data.get_category(src)
            # For each sensor in the const definition
            for sensor_type, sensors_list in sensors.items():
                for sensorName, params in sensors_list.items():
                    # Check if the sensor exists in the capabilities
                    if sensorName == src:
                        entities.append(
                            ApplianceSensor(
                                name=f"{data.get_name()} {data.get_sensor_name(sensorName, src)}",
                                attr=sensorName,
                                field=params[0],
                                device_class=params[1],
                                entity_category=sensor_type,
                                unit=params[2],
                                source=category,
                            )
                        )
            for sensor_type, sensors_list in sensors_binary.items():
                for sensorName, params in sensors_list.items():
                    if sensorName == src:
                        entities.append(
                            ApplianceBinary(
                                name=f"{data.get_name()} {data.get_sensor_name(sensorName, src)}",
                                attr=sensorName,
                                field=params[0],
                                device_class=params[1],
                                entity_category=sensor_type,
                                invert=params[2],
                                source=category,
                            )
                        )
            if src == "executeCommand":
                commands : dict[str, str] = data.capabilities[src]["values"]
                commands_keys = list(commands.keys())
                for command in commands_keys:
                    entities.append(
                        ApplianceButton(
                            name=f"{data.get_name()} {command}",
                            attr='ExecuteCommand',
                            val_to_send=command,
                            source=category,
                            icon=icon_mapping.get(command, "mdi:gesture-tap-button"),
                        )
                    )
        # Setup each found entities
        self.entities = [
            entity.setup(data)
            for entity in entities
        ]

class Appliances:
    def __init__(self, found_appliances:  dict[str, Appliance]) -> None:
        self.found_appliances = found_appliances

    def get_appliance(self, pnc_id):
        return self.found_appliances.get(pnc_id, None)
