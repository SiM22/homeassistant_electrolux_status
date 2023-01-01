"""The electrolux Status constants."""
from homeassistant.const import TIME_MINUTES, TEMP_CELSIUS, PERCENTAGE
from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_CONNECTIVITY,
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_LOCK,
)
from homeassistant.components.sensor import SensorDeviceClass

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
    "TimeToEnd": [None, None, TIME_MINUTES],
    "RunningTime": [None, None, TIME_MINUTES],
    "CyclePhase": [None, None, None],
    "CycleSubPhase": ["string", None, None],
    "ApplianceState": [None, None, None],
    "RemoteControl": [None, None, None],
    "DisplayTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
    "DisplayFoodProbeTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
    "SensorTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
    "TargetTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
    "DefrostTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS],
}

sensors_binary = {
# Sensor Name: [value field, device class, invert]
    "DoorState": ["numberValue", DEVICE_CLASS_DOOR, None],
    "DoorLock":  ["numberValue", DEVICE_CLASS_LOCK, True],
}

sensors_diagnostic = {
# Sensor Name: [value field, device class, unit]
    "SensorHumidity": ["numberValue", SensorDeviceClass.HUMIDITY, PERCENTAGE, None],
    "AmbientTemperature": ["container", SensorDeviceClass.TEMPERATURE, TEMP_CELSIUS, None],
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
