"""The electrolux Status constants."""
from homeassistant.const import UnitOfTime
from homeassistant.const import UnitOfTemperature
from homeassistant.const import UnitOfPower
from homeassistant.const import PERCENTAGE
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
CONF_LANGUAGE = "language"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_LANGUAGE = "English"

# capabilities model :
#
# key = "entry" or "category/entry"
# {
#   access = "read" or "readwrite" or "write" (other values ignored)
#   type = "boolean" or "string" or "number" (other values ignored including "int" type only used in maintenance section)
#   => problem to differentiate classic numbers to time : check after "time" string in key name ? or temperature
#   values (optional)= list of available values
#   min / max / step for type = number
# }

sensors = {
# Sensor Name: [value field, device class, unit]
# Device state sensors
    None: {
        "timeToEnd": [None, None, UnitOfTime.MINUTES],
        "runningTime": [None, None, UnitOfTime.MINUTES],
        "cyclePhase": [None, None, None],
        "cycleSubPhase": ["string", None, None],
        "applianceState": [None, None, None],
        "displayTemperature": ["container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "displayFoodProbeTemperature": ["container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "sensorTemperature": ["container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "defrostTemperature": ["container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "targetMicrowavePower": ["numberValue", SensorDeviceClass.ENERGY, UnitOfPower.WATT],
        "ovenProcessIdentifier": ["valueTransl", None, None],
        "remoteControl": [None, None, None],
        "defaultExtraRinse": ["numberValue", None, None],
        "targetTemperature": ["container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "startTime": [None, None, UnitOfTime.MINUTES],
        "analogTemperature": ["numberValue", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "waterSoftenerMode": [None, None, None],
        "steamValue": ["valTransl", None, None],
        "eLUXTimeManagerLevel": ["valTransl", None, None],
        "analogSpinSpeed": ["valTransl", None, None],
        "waterTankWarningMode": [None, None, None],
        "dryingTime": [None, None, None],
        "humidityTarget": ["valTransl", None, None],
        "antiCreaseValue": [None, None, None],
        "drynessValue": ["valTransl", None, None],
        "programUID": ["valTransl", None, None]
    },
# Device diagnostic sensors
    EntityCategory.DIAGNOSTIC : {
        "sensorHumidity": ["numberValue", SensorDeviceClass.HUMIDITY, PERCENTAGE, None],
        "ambientTemperature": ["container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, None],
        "applianceTotalWorkingTime": [None, None, UnitOfTime.MINUTES],
        "totalCycleCounter": [None, None, None],
        "rinseAidLevel": [None, None, None],
        "waterHardness": ["valueTransl", None, None],
        "fCTotalWashCyclesCount": [None, None, None],
        "fCTotalWashingTime": [None, None, None],
        "applianceMode": [None, None, None],
    }
}


sensors_binary = {
# Sensor Name: [value field, device class, invert]
# Device state sensors
    None: {
        "doorState": ["numberValue", BinarySensorDeviceClass.DOOR, None],
        "doorLock":  ["numberValue", BinarySensorDeviceClass.LOCK, True],
        "uiLockMode": ["numberValue", None, None],
        "endOfCycleSound": ["numberValue", None, None],
        "defaultSoftPlus": ["numberValue", None, None],
        "preWashPhase": ["numberValue", None, None],
        "rinseHold": ["numberValue", None, None],
        "nightCycle": ["numberValue", None, None],
        "stain": ["numberValue", None, None],
        "wMEconomy": ["numberValue", None, None],
        "anticreaseWSteam": ["numberValue", None, None],
        "anticreaseNoSteam": ["numberValue", None, None],
        "refresh": ["numberValue", None, None],
        "reversePlus": ["numberValue", None, None],
        "delicate": ["numberValue", None, None],
        "tDEnergyLabel": ["numberValue", None, None],
        "tDEconomy_Eco": ["numberValue", None, None],
        "tDEconomy_Night": ["numberValue", None, None],
    },
# Device diagnostic sensors
    EntityCategory.DIAGNOSTIC : {
        "tankA_reserve": ["numberValue", BinarySensorDeviceClass.PROBLEM, False],
        "tankB_reserve": ["numberValue", BinarySensorDeviceClass.PROBLEM, False],
    }
}

icon_mapping = {
    "OFF": "mdi:power-off",
    "ON": "mdi:power-on",
    "START": "mdi:play",
    "STOPRESET": "mdi:stop",
    "PAUSE": "mdi:pause",
    "RESUME": "mdi:play-pause",
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
