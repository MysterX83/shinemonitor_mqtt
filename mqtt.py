from paho.mqtt import client as mqtt_client
import config
import random


def on_publish(client, userdata, result):  # create function for callback
    pass


def on_disconnect(client, userdata, rc):
    pass


def connect_mqtt(log):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info("Connected to MQTT Broker!")
        else:
            log.error("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    # Client id
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username=config.mqtt_broker_user, password=config.mqtt_broker_password)
    client.on_connect = on_connect
    client.connect(config.mqtt_broker_url, config.mqtt_broker_port)
    return client


def publish(log, client, topic, message):
    result = client.publish(topic, message)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        log.info(f"Send `{message}` to topic `{topic}`")
    else:
        log.error(f"Failed to send message to topic {topic}")
