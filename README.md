# Shinemonitor_mqtt
This python script gets data from shinemonitor and published it to a MQTT broker.

**This code is created for private use, there will be no support. 
Create copies where you like.**

## Config
use config.py to set the right config.

### Log config
- log_path = The path to place the log file

### MQTT config
- mqtt_broker_url = URL of your mqtt broker
- mqtt_broker_port = PORT of your mqtt broker
- mqtt_broker_user = Username to login on your mqtt broker
- mqtt_broker_password = Password to login on your mqtt broker
- topic_actual = MQTT topic to publish actual power info
- topic_total = MQTT topic to publish total energy info

### Shinemonitor config
- baseURL = base url of shinemonitor website
- usr = username of the shinemonitor website
- pwd = password of the shinemonitor website
- companykey = Companykey. Obtained from portal
- plantId = Plant id (Power station ID). Obtained from portal.
- pn = Datalogger PN number. Obtained from portal
- sn = Device serial number. Obtained from portal
- devcode = Device coding. Obtained from portal
