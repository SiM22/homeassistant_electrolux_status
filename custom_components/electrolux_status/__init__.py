"""electrolux status integration."""
from pyelectroluxconnect import Session

import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .pyelectroluxconnect_util import pyelectroluxconnect_util
from .api import Appliance, Appliances, ElectroluxLibraryEntity
from .const import CONF_PASSWORD, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, CONF_REGION, DEFAULT_REGION
from .const import CONF_LANGUAGE, DEFAULT_LANGUAGE
from .const import CONF_USERNAME
from .const import DOMAIN
from .const import PLATFORMS
from .const import languages

_LOGGER: logging.Logger = logging.getLogger(__package__)


# noinspection PyUnusedLocal
async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    if entry.options.get(CONF_SCAN_INTERVAL):
        update_interval = timedelta(seconds=entry.options[CONF_SCAN_INTERVAL])
    else:
        update_interval = timedelta(seconds=DEFAULT_SCAN_INTERVAL)

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)
    region = entry.data.get(CONF_REGION, DEFAULT_REGION)
    language = languages.get(entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),"eng")

    client = pyelectroluxconnect_util.get_session(username, password, region, language)

    coordinator = ElectroluxStatusDataUpdateCoordinator(hass, client=client, update_interval=update_interval)
    if not await coordinator.async_login():
        raise ConfigEntryAuthFailed

    await coordinator.async_config_entry_first_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    coordinator.platforms.extend(PLATFORMS)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.add_update_listener(async_reload_entry)
    return True


class ElectroluxStatusDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, client: Session, update_interval: timedelta) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def async_login(self) -> bool:
        try:
            await self.hass.async_add_executor_job(self.api.login)
        except Exception as ex:
            _LOGGER.error("Could not log in to ElectroluxStatus, %s", ex)
            return False
        return True

    async def _async_update_data(self):
        """Update data via library."""
        await self.async_login()
        found_appliances = {}
        try:
            appliances_json = await self.hass.async_add_executor_job(self.api.getAppliances)
            for appliance in appliances_json:
                connection_state = await self.hass.async_add_executor_job(self.api.getApplianceConnectionState, appliance)
                appliance_state = await self.hass.async_add_executor_job(self.api.getApplianceState, appliance)
                appliance_profile = await self.hass.async_add_executor_job(self.api.getApplianceProfile, appliance)
                appliance_name = appliances_json[appliance]['alias'] or appliance
                appliance_model = appliances_json[appliance]['model'] or appliances_json[appliance]['pnc']
                app = Appliance(appliance_name, appliance, appliances_json[appliance]['brand'], appliance_model)
                app.setup(ElectroluxLibraryEntity(appliance_name, connection_state, appliance_state, appliance_profile))
                found_appliances[appliance_name] = app
            return {
                "appliances": Appliances(found_appliances)
            }
        except Exception as exception:
            _LOGGER.exception(exception)
            raise UpdateFailed() from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
