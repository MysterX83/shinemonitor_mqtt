#!/usr/bin/python3
from datetime import datetime

import config
import logger
import shinemonitor
import mqtt


def run():
    log = logger.create_rotating_log(config.log_path)
    log.info("started")

    token, secret, expire = shinemonitor.login(log)
    client = mqtt.connect_mqtt(log)
    client.loop_start()

    while True:
        try:
            now = datetime.now()
            if now > expire:
                log.info("token expired: " + expire + " , " + str(now))
                token, secret, expire = shinemonitor.login(log)

            energy_now_msg = shinemonitor.get_energy_now(log, token, secret)
            mqtt.publish(log, client, config.topic_actual, energy_now_msg)

            energy_total_msg = shinemonitor.get_energy_total(log, token, secret)
            mqtt.publish(log, client, config.topic_total, energy_total_msg)
        except:
            log.error("Exception occurred, try login again.")
            token, secret, expire = shinemonitor.login(log)

if __name__ == '__main__':
    run()
