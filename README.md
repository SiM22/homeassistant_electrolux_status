# Home Assistant Electrolux Care Integration (Not Official)

[![Validate with HACS](https://github.com/mauro-midolo/homeassistant_electrolux_status/actions/workflows/hacs.yml/badge.svg)](https://github.com/mauro-midolo/homeassistant_electrolux_status/actions/workflows/hacs.yml)
[![Validate with hassfest](https://github.com/mauro-midolo/homeassistant_electrolux_status/actions/workflows/hassfest.yml/badge.svg)](https://github.com/mauro-midolo/homeassistant_electrolux_status/actions/workflows/hassfest.yml)

This is an integration to Home Assistant to communicate with the Electrolux Connectivity Platform (ECP), Electrolux owned brands, like: Electrolux, AEG, Frigidaire, Husqvarna.

Tested with Electrolux and AEG washer-dryer, but probably could be used with some internet connected ovens, diswashers, fridges, airconditioners.

### Supported and tested devices

- ELECTROLUX EDH803BEWA - UltimateCare 800
- ELECTROLUX EW9H283BY - PerfectCare 900
- ELECTROLUX EWF1041ZDWA - UltimateCare 900 AutoDose
- AEG L6FBG841CA - 6000 Series Autodose
- AEG L7FENQ96 - 7000 Series ProSteam Autodose

## Prerequisites
- All devices need configured into "My Electrolux Care" application
- All devices need Alias set into "My Electrolux Care" application (otherwise the home assistant integration raises the authentication error)

## Installation
1. Click install.
2. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Electrolux status".
3. Insert the Electrolux Care Application credentials

## Thanks
This integration uses the following Python Library:
* [https://pypi.org/project/pyelectroluxconnect/](https://pypi.org/project/pyelectroluxconnect/)

## Disclaimer
This Home Assistant integration was not made by Electrolux. It is not official, not developed, and not supported by Electrolux.
