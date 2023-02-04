# Home Assistant Electrolux Care Integration (Not Official)

[![Validate with HACS](https://github.com/mauro-midolo/homeassistant_electrolux_status/actions/workflows/hacs.yml/badge.svg)](https://github.com/mauro-midolo/homeassistant_electrolux_status/actions/workflows/hacs.yml)
[![Validate with hassfest](https://github.com/mauro-midolo/homeassistant_electrolux_status/actions/workflows/hassfest.yml/badge.svg)](https://github.com/mauro-midolo/homeassistant_electrolux_status/actions/workflows/hassfest.yml)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=mauro-midolo_homeassistant_electrolux_status&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=mauro-midolo_homeassistant_electrolux_status)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=mauro-midolo_homeassistant_electrolux_status&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=mauro-midolo_homeassistant_electrolux_status)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=mauro-midolo_homeassistant_electrolux_status&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=mauro-midolo_homeassistant_electrolux_status)

[![Donate](https://img.shields.io/static/v1?label=PayPal&message=Buy%20Me%20a%20Coffee&color=green&logo=PayPal)](https://paypal.me/mauromi?country.x=IT&locale.x=it_IT)

This is an integration to Home Assistant to communicate with the Electrolux Connectivity Platform (ECP), Electrolux owned brands, like: Electrolux, AEG, Frigidaire, Husqvarna.

Tested with Electrolux and AEG washer-dryer, but probably could be used with some internet connected ovens, diswashers, fridges, airconditioners.

### Supported and tested devices

- ELECTROLUX EDH803BEWA - UltimateCare 800
- ELECTROLUX EW9H283BY - PerfectCare 900
- ELECTROLUX EWF1041ZDWA - UltimateCare 900 AutoDose
- ELECTROLUX EEM69410W - MaxiFlex 700
- ELECTROLUX EOD6P77WZ - SteamBake 600
- ELECTROLUX KODDP77WX - SteamBake 600
- ELECTROLUX EHE6799SA - 609L UltimateTaste 900
- ELECTROLUX EW9H869E9 - PerfectCare 900 Dryer
- ELECTROLUX EW9H188SPC - PerfectCare 900 Dryer
- ELECTROLUX EW8F8669Q8 - PerfectCare 800 Washer
- ELECTROLUX EW9F149SP - PerfectCare 900 Washer
- Electrolux KEGB9300W - Dishwasher
- Electrolux EEG69410W - Dishwasher 
- AEG L6FBG841CA - 6000 Series Autodose
- AEG L7FENQ96 - 7000 Series ProSteam Autodose
- AEG L7FBE941Q - 7000 Series Prosense Autodose
- AEG L8FEC96QS - 8000 Series Ökomix Autodose
- AEG L9WBA61BC - 9000 Series ÖKOKombi DualSense SensiDry
- AEG BPE558370M - SteamBake 6000

## Prerequisites
All devices need configured and Alias set (otherwise the home assistant integration raises the authentication error) into following applications (depends on device type and region):
- My Electrolux Care/My AEG Care (EMEA region)
- Electrolux Kitchen/AEG Kitchen (EMEA region)
- Electrolux Life (APAC region)
- Electrolux Home+ (LATAM region)
- Electrolux Oven/Frigidaire 2.0 (NA region)

## Installation
1. Click install.
2. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Electrolux status".
3. Insert the Electrolux Care Application credentials

## Thanks
This integration uses the following Python Library:
* [https://pypi.org/project/pyelectroluxconnect/](https://pypi.org/project/pyelectroluxconnect/)

## Disclaimer
This Home Assistant integration was not made by Electrolux. It is not official, not developed, and not supported by Electrolux.

## Support the project with a donation
This project is open source and free, but if you want to support us and help us continue to maintain and improve it, you can make a donation through PayPal. 
Any contribution, no matter how small, is greatly appreciated and will help us keep the project active and healthy. Thank you for your support!

[![Donate](https://img.shields.io/static/v1?label=PayPal&message=Buy%20Me%20a%20Coffee&color=green&logo=PayPal)](https://paypal.me/mauromi?country.x=IT&locale.x=it_IT)

