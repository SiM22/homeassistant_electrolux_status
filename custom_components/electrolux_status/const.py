"""The electrolux Status constants."""
from enum import StrEnum
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

class ApplianceState(StrEnum):
    ALARM = "Alarm"
    DELAYED_START = "Delayed start"
    END_OF_CYCLE = "End of cycle"
    IDLE = "Idle"
    OFF = "Off"
    PAUSED = "Paused"
    READY_TO_START = "Read to start"
    RUNNING = "Running"

class HumidityTarget(StrEnum):
    CUPBOARD = "Cupboard dry"
    EXTRA = "Extra dry"
    IRON = "Iron dry"
    UNDEFINED = "Undefined"

class ProgramUID(StrEnum):
    AUTO_EASY_IRON_PR_EASYIRON = "Easy iron"
    BED_LINEN_PLUS_PR_BEDDINGPLUS = "Bed linen XL"
    BLANKET_PR_BEDDING = "Duvet"
    COTTON_PR_COTTONS = "Cottons"
    COTTON_PR_ENERGYSAVER = "Cottons eco"
    COTTON_PR_ENERGY_SAVER = "Cottons eco"
    COTTON_PR_TOWELS = "Towels"
    COTTON_PR_WORKINGCLOTHES = "Workwear"
    DELICATE_PR_BABYCARE = "Baby"
    DELICATE_PR_CURTAINS = "Curtains"
    DELICATE_PR_DELICATES = "Delicates"
    DELICATE_PR_SOFTTOYS = "Soft toys"
    DOWN_JACKET_PR_DOWN_JACKET = "Down jackets"
    DRUM_CLEAN_PR_TUB_CLEAN = "Machine clean"
    DRY_CLEANING_PR_REFRESH = "Refresh"
    DUVET_PR_DUVET = "Duvet"
    DUVET_PR_HYGENICCARE = "Hygiene"
    EXPRESS_PR_DAILY39 = "Daily 39"
    EXPRESS_PR_FULLWASH60 = "Full Wash 60"
    EXTRA_DELICATE_PR_DELICATES = "Delicates"
    FLEECE_PR_FLEECE = "Fleece"
    JEANS_PR_DENIM = "Denim"
    OUTD_PROOF_PR_OUTDOOR = "Outdoor"
    RAPID_PR_QUICK_15MIN = "Quick 15"
    SANITISE60_PR_ANTIALLERGY = "Anti-allergy"
    SHIRTS_PR_BUSINESSSHIRT = "Business shirts"
    SILK_DRY_PR_SILK = "Silk"
    SOFTENER_PR_RINSE = "Rinse"
    SPIN_PR_SPIN = "Spin"
    SPORTS_PR_MICROFIBRE = "Microfibre"
    SPORTS_PR_SPORT = "Sports"
    SPORT_JACKETS_PR_OUTDOOR = "Outdoor"
    STEAM_DEWRINKLER_PR_VAPOURREFRESH = "Vapour refresh"
    SYNTHETIC_PR_MIXED = "Mixed"
    SYNTHETIC_PR_SPORT = "Sports"
    SYNTHETIC_PR_SYNTHETICS = "Synthetics"
    TIMEDRY_PR_DRYINGRACK = "Drying Rack"
    TOWELS_PR_TOWELS = "Towels"
    UNIVERSAL_PR_MIXEDPLUSNOTXL = "Mixed XL"
    WOOL_GOLD_PR_WOOL = "Wool"
    WOOL_PR_WOOL = "Wool / Silk"
    WORKINGCLOTHES_PR_WORKINGCLOTHES = "Workwear"

class SteamValue(StrEnum):
    STEAM_OFF = "Off"
    STEAM_MED = "On"

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
        "timeToEnd": [None, None, None, UnitOfTime.MINUTES],
        "runningTime": [None, None, None, UnitOfTime.MINUTES],
        "cyclePhase": [None, "string", None, None],
        "cycleSubPhase": [None, "string", None, None],
        "applianceState": [None, ApplianceState, None, None],
        "displayTemperature": [None, "container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "displayFoodProbeTemperature": [None, "container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "sensorTemperature": [None, "container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "defrostTemperature": [None, "container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "targetMicrowavePower": [None, None, SensorDeviceClass.ENERGY, UnitOfPower.WATT],
        "ovenProcessIdentifier": [None, None, None, None],
        "remoteControl": [None, "string", None, None],
        "defaultExtraRinse": [None, None, None, None],
        "targetTemperature": [None, "container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS],
        "startTime": [None, None, None, UnitOfTime.MINUTES],
        "analogTemperature": ["Temperature", None, None, None],
        "waterSoftenerMode": [None, None, None, None],
        "steamValue": ["Vapour", SteamValue, None, None],
        "eLUXTimeManagerLevel": [None, None, None, None],
        "analogSpinSpeed": ["Spin speed", "string", None, None],
        "waterTankWarningMode": [None, None, None, None],
        "dryingTime": [None, None, None, None],
        "humidityTarget": ["Sensor Dry", HumidityTarget, None, None],
        "antiCreaseValue": ["Anti-crease", None, None, None],
        "drynessValue": ["Dryness Level", "string", None, None],
        "programUID": ["Programme", ProgramUID, None, None]
    },
# Device diagnostic sensors
    EntityCategory.DIAGNOSTIC : {
        "sensorHumidity": [None, None, SensorDeviceClass.HUMIDITY, PERCENTAGE, None],
        "ambientTemperature": [None, "container", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, None],
        "applianceTotalWorkingTime": [None, None, None, UnitOfTime.MINUTES],
        "totalCycleCounter": [None, None, None, None],
        "rinseAidLevel": [None, None, None, None],
        "waterHardness": [None, "string", None, None],
        "applianceMode": [None, None, None, None],
    }
}


sensors_binary = {
# Sensor Name: [value field, device class, invert]
# Device state sensors
    None: {
        "doorState": [None, None, BinarySensorDeviceClass.DOOR, None],
        "doorLock":  [None, None, BinarySensorDeviceClass.LOCK, True],
        "uiLockMode": [None, None, None, None],
        "endOfCycleSound": [None, None, None, None],
        "defaultSoftPlus": [None, None, None, None],
        "preWashPhase": ["Prewash", None, None, None],
        "rinseHold": [None, None, None, None],
        "nightCycle": [None, None, None, None],
        "stain": ["Stains", None, None, None],
        "wMEconomy": [None, None, None, None],
        "anticreaseWSteam": [None, None, None, None],
        "anticreaseNoSteam": [None, None, None, None],
        "refresh": [None, None, None, None],
        "reversePlus": [None, None, None, None],
        "delicate": [None, None, None, None],
        "tcSensor": ["SensorWash", None, None, None],
        "ultraMix": ["Ultramix", None, None, None],
        "tDEnergyLabel": [None, None, None, None],
        "tDEconomy_Eco": [None, None, None, None],
        "tDEconomy_Night": ["Extra Silent", None, None, None],
    },
# Device diagnostic sensors
    EntityCategory.DIAGNOSTIC : {
        "tankA_reserve": [None, None, BinarySensorDeviceClass.PROBLEM, False],
        "tankB_reserve": [None, None, BinarySensorDeviceClass.PROBLEM, False],
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
