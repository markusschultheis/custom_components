# Home Assistant Viessmann Gridbox Addon
**Not an official Viessmann Addon**

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Funl0ck%2Fhomeassistant-addon-viessmann-gridbox)

## Add-ons
### [GridboxConnector add-on](./viessmann_pv)

# Viessmann GridX Integration
Diese Integration ist für die Darstellung von PV-Anlagendaten gedacht. 
Die PV-Anlage ist mittels Gridbox mit dem Internet verbunden und sendet die Daten an GridX, welches der zentrale Datensammler fuer das Unternehmen Viessmann ist. Wir benutzen also die API von GridX, um unsere eigenen Anlagendaten abzurufen und in Home Assistant bereitzustellen. Von dort aus koennen die Daten dann zum beispiel im Energy Monitoring aufgenommen und dargestellt werden. 
Ein weiterer Anwendungsfall ist beispielsweise die Daten in Grafana zur weiteren Auswertung bereitzustellen.

{
 'batteries': 
    [
       {
       'applianceID': 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
       'capacity': x, 
       'nominalCapacity': x,
       'power': x, 
       'remainingCharge': x, 
       'stateOfCharge': x
       }
    ], 
 'battery': 
     {
     'capacity': 0, 
     'nominalCapacity': 0,
     'power': 0, 
     'remainingCharge': 0, 
     'stateOfCharge': 0
     }, 
     'consumption': x, 
     'directConsumption': 0,
    'directConsumptionEV': 0, 
    'directConsumptionHeatPump': 0, 
    'directConsumptionHeater': 0, 
    'directConsumptionHousehold': 0, 
    'grid': 0,
    'gridMeterReadingNegative': 0, 
    'gridMeterReadingPositive': 0, 
    'heatPump': 0, 
    'heatPumps': 
        [
         {
          'applianceID': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx', 
          'power': 0, 
          'sgReadyState': 
          'UNKNOWN'
         }
        ],
    'l1CurtailmentPower': 0, 
    'l2CurtailmentPower': 0, 
    'l3CurtailmentPower': 0, 
    'measuredAt': '2025-02-22T20:25:21Z', 
    'photovoltaic': 0, 
    'production': 0, 
    'selfConsumption': 0, 
    'selfSufficiencyRate': 0,
    'selfSupply': 0, 
    'totalConsumption': 0
}  
