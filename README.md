# ha_custom_components
Diese Integration ist für die Darstellung von PV-Anlagendaten gedacht. 
Der konkrete Anwendungsfall:

Die PV-Anlage ist mittels einer Gridbox mit dem Internet verbunden und erfasst somit sämtliche Leistungsdaten der Anlage.
{'batteries': [{'applianceID': 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 'capacity': x, 'nominalCapacity': x, 'power': x, 'remainingCharge': x, 'stateOfCharge': x}], 
'battery': {'capacity': 0, 'nominalCapacity': 0, 'power': 0, 'remainingCharge': 0, 'stateOfCharge': 0}, 
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
'heatPumps': [{'applianceID': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx', 'power': 0, 'sgReadyState': 'UNKNOWN'}],
'l1CurtailmentPower': 0, 
'l2CurtailmentPower': 0, 
'l3CurtailmentPower': 0, 
'measuredAt': '2025-02-22T20:25:21Z', 
'photovoltaic': 0, 
'production': 0, 
'selfConsumption': 0, 
'selfSufficiencyRate': 0,
'selfSupply': 0, 
'totalConsumption': 0}  
