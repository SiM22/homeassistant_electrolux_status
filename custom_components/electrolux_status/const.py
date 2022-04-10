"""The electrolux Status constants."""
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
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_NAME = DOMAIN
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_REGION = "emea"

icon_mapping = {
    "Pause": "mdi:pause",
    "Resume": "mdi:play-pause",
    "Start": "mdi:play",
    "Stop": "mdi:stop",
    "TURN ON": "mdi:power-on",
    "ON": "mdi:power-on",
    "TURN OFF": "mdi:power-off",
    "OFF": "mdi:power-off"}
