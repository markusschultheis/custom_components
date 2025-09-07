# Home Assistant Viessmann Gridbox Addon
**Not an official Viessmann Addon**

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Funl0ck%2Fhomeassistant-addon-viessmann-gridbox)

## Add-ons
### [Viessmann PV-Anlage](./gridx)
# Setup
Im Haushalt ist ein Viessmann Wechselrichter, sowie eine Luftwaermepumpe installiert. Diese Geraete sind mit einer GridX-Box verbunden. 

# Viessmann GridX Integration: Was macht die Integration?
Diese Integration ruft die PV-Anlagendaten ueber die GridX-API ab. Die Anlagedaten werden dann in Home Assistant zur weiteren Ver-/Bearbeitung zur Verfuegung gestellt. 

# Anwendungsfall:
# a) Bei einer Luft-Wärmepumpe kann PV-Überschuss genutzt werden, um die Warmwasserbereitung zu unterstützen, indem überschüssiger Solarstrom direkt für den Betrieb der Wärmepumpe eingesetzt wird. 

1. PV-Überschuss erkennen:
   Sensoren oder Smart-Home-Systeme messen die aktuelle PV-Leistung und den Eigenverbrauch. Wenn die Einspeisung ins Netz negativ wird (also Überschuss vorhanden ist), wird dies
   erkannt.
2. Warmwasser-Bedarf prüfen:
   Das System überprüft, ob Warmwasser benötigt wird, z. B. über den Temperatursensor im Speicher oder über geplante Boost-Zeiten.
3. Boost aktivieren:
   Liegt Überschuss vor, schaltet das System die Wärmepumpe gezielt für die Warmwasserbereitung ein („Warmwasser-Boost“), auch wenn sonst vielleicht keine Heizung oder
   Warmwasserbereitung nötig wäre.
4. Strom sparen / Einspeisung reduzieren:
   Dadurch wird überschüssiger PV-Strom genutzt. Statt ihn ins Netz einzuspeisen wird der Eigenverbrauch gesteigert.

# b) Ein weiterer Anwendungsfall: Datenbereitstellung in Grafana zur weiteren Auswertung.

Daten die mittels API Call abgerufen werden:
-----------------------------------------------------------------------------------------
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
    'measuredAt': 'XXXX-XX-XXTXX:XX:XXZ', 
    'photovoltaic': 0, 
    'production': 0, 
    'selfConsumption': 0, 
    'selfSufficiencyRate': 0,
    'selfSupply': 0, 
    'totalConsumption': 0
}  


<img width="2258" height="1146" alt="image" src="https://github.com/user-attachments/assets/007a8005-7844-4d54-9f2f-74a7f563475e" />

