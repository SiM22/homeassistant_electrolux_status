"""The electrolux Status constants."""
from homeassistant.const import TIME_MINUTES, TEMP_CELSIUS, PERCENTAGE, POWER_WATT

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

# Base component constants
NAME = "Elettrolux status"
DOMAIN = "electrolux_status"
DOMAIN_DATA = f"{DOMAIN}_data"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
BUTTON = "button"
PLATFORMS = [BINARY_SENSOR, SENSOR, BUTTON]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_REGION = "region"
CONF_LANGUAGE = "language"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_REGION = "emea"
DEFAULT_LANGUAGE = "English"

sensors = {
# Sensor Name: [value field, device class, unit]
# Device state sensors
    None: {
        "TimeToEnd": [None, None, TIME_MINUTES],
        "RunningTime": [None, None, TIME_MINUTES],
        "CyclePhase": [None, None, None],
        "CycleSubPhase": ["string", None, None],
        "ApplianceState": [None, None, None],
        "DisplayTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
        "DisplayFoodProbeTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
        "SensorTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
        "DefrostTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
        "TargetMicrowavePower": ["numberValue", SensorDeviceClass.ENERGY, POWER_WATT],
        "OvenProcessIdentifier": ["valueTransl", None, None],
    },
# Device config sensors
    EntityCategory.CONFIG : {
        "RemoteControl": [None, None, None],
        "DefaultExtraRinse": ["numberValue", None, None],
        "TargetTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
        "StartTime": [None, None, TIME_MINUTES],
        "AnalogTemperature": ["numberValue", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
        "WaterSoftenerMode": [None, None, None],
        "SteamValue": ["valTransl", None, None],
        "ELUXTimeManagerLevel": ["valTransl", None, None],
        "AnalogSpinSpeed": ["valTransl", None, None],
        "WaterTankWarningMode": [None, None, None],
        "DryingTime": [None, None, None],
        "HumidityTarget": ["valTransl", None, None],
        "AntiCreaseValue": [None, None, None],
        "DrynessValue": ["valTransl", None, None],
        "ProgramUID": ["valTransl", None, None]
    },
# Device diagnostic sensors
    EntityCategory.DIAGNOSTIC : {
        "SensorHumidity": ["numberValue", SensorDeviceClass.HUMIDITY, PERCENTAGE, None],
        "AmbientTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS, None],
        "ApplianceTotalWorkingTime": [None, None, TIME_MINUTES],
        "TotalCycleCounter": [None, None, None],
        "RinseAidLevel": [None, None, None],
        "WaterHardness": ["valueTransl", None, None],
        "FCTotalWashCyclesCount": [None, None, None],
        "FCTotalWashingTime": [None, None, None],
        "ApplianceMode": [None, None, None],
    }
}


sensors_binary = {
# Sensor Name: [value field, device class, invert]
# Device state sensors
    None: {
        "DoorState": ["numberValue", BinarySensorDeviceClass.DOOR, None],
        "DoorLock":  ["numberValue", BinarySensorDeviceClass.LOCK, True],
        "UiLockMode": ["numberValue", None, None],
    },
# Device config sensors
    EntityCategory.CONFIG : {
        "EndOfCycleSound": ["numberValue", None, None],
        "DefaultSoftPlus": ["numberValue", None, None],
        "PreWashPhase": ["numberValue", None, None],
        "RinseHold": ["numberValue", None, None],
        "NightCycle": ["numberValue", None, None],
        "Stain": ["numberValue", None, None],
        "WMEconomy": ["numberValue", None, None],
        "AnticreaseWSteam": ["numberValue", None, None],
        "AnticreaseNoSteam": ["numberValue", None, None],
        "Refresh": ["numberValue", None, None],
        "ReversePlus": ["numberValue", None, None],
        "Delicate": ["numberValue", None, None],
        "TDEnergyLabel": ["numberValue", None, None],
        "TDEconomy_Eco": ["numberValue", None, None],
        "TDEconomy_Night": ["numberValue", None, None],
    },
# Device diagnostic sensors
    EntityCategory.DIAGNOSTIC : {
        "TankA_reserve": ["numberValue", BinarySensorDeviceClass.PROBLEM, False],
        "TankB_reserve": ["numberValue", BinarySensorDeviceClass.PROBLEM, False],
    }
}

icon_mapping = {
    "0": "mdi:power-off",
    "1": "mdi:power-on",
    "2": "mdi:play",
    "3": "mdi:stop",
    "4": "mdi:pause",
    "5": "mdi:play-pause",
}

# List of supported Mobile App languages (from https://emea-production.api.electrolux.net/masterdata-service/api/v1/languages)
languages = {
    "български": "bul",
    "český": "ces",
    "Dansk": "dan",
    "Deutsch": "deu",
    "ελληνικός": "ell",
    "English": "eng",
    "eesti": "est",
    "Soome": "fin",
    "Français": "fra",
    "Hrvatski": "hrv",
    "magyar": "hun",
    "Italiano": "ita",
    "lettone": "lav",
    "lituano": "lit",
    "Luxembourgish": "ltz",
    "nederlands": "nld",
    "Norsk": "nor",
    "Polski": "pol",
    "Português": "por",
    "Română": "ron",
    "rusesc": "rus",
    "slovenský": "slk",
    "slovinský": "slv",
    "Español": "spa",
    "Svenska": "swe",
    "Türk": "tur",
    "Ukrayna": "ukr",
}
