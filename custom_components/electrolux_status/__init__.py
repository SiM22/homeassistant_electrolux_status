"""electrolux status integration."""
import json

from pyelectroluxocp import OneAppApi

import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed
from pyelectroluxocp.apiModels import ApplienceStatusResponse

from .pyelectroluxconnect_util import pyelectroluxconnect_util
from .api import Appliance, Appliances, ElectroluxLibraryEntity
from .const import CONF_PASSWORD, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
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
    language = languages.get(entry.data.get(CONF_LANGUAGE, DEFAULT_LANGUAGE),"eng")

    client = pyelectroluxconnect_util.get_session(username, password, language)

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
    api: OneAppApi = None

    def __init__(self, hass: HomeAssistant, client: OneAppApi, update_interval: timedelta) -> None:
        """Initialize."""
        self.api = client
        self.platforms = []

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    async def async_login(self) -> bool:
        try:
            await self.hass.async_add_executor_job(self.api.get_appliances_list)
        except Exception as ex:
            _LOGGER.error("Could not log in to ElectroluxStatus, %s", ex)
            return False
        return True

    async def _async_update_data(self):
        """Update data via library."""
        await self.async_login()
        found_appliances = {}
        try:
            appliances_json:list[ApplienceStatusResponse] = await self.api.get_appliances_list()
            _LOGGER.debug("Electrolux update appliances %s", json.dumps(appliances_json))
            for appliance in appliances_json:
                connection_state = appliance.get('connectionState')
                # appliance_state = appliance.get('properties').get('reported').get('applianceState')
                # appliance_profile = await self.hass.async_add_executor_job(self.api.getApplianceProfile, appliance)
                appliance_name = appliance.get('applianceData').get('applianceName')
                appliance_infos = await self.api.get_appliances_info([appliance.get('applianceId')])
                appliance_capabilities = await self.api.get_appliance_capabilities(appliance.get('applianceId'))
                appliance_status = await self.api.get_appliance_status(appliance.get('applianceId'))
                appliance_info = None if len(appliance_infos) == 0 else appliance_infos[0]
                appliance_model = appliance_info.get('model') if appliance_info else ""
                brand = appliance_info.get('brand') if appliance_info else ""
                # appliance_profile not reported
                app = Appliance(appliance_name, appliance_status, brand, appliance_model)
                app.setup(ElectroluxLibraryEntity(appliance_name, connection_state, appliance_status,
                                                  appliance_info, appliance_capabilities))
                found_appliances[appliance_name] = app
            _LOGGER.debug("Electrolux found appliances %s", ", ".join(list(found_appliances.keys())))
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
