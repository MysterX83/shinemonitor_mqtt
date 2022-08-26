import hashlib
import requests
import time as time_
from datetime import datetime, timedelta
import config


def salt():
    return int(round(time_.time() * 1000))


def gettoken(log, salt_str):
    # Build auth url
    pow_sha1 = hashlib.sha1()
    pow_sha1.update(config.pwd.encode('utf-8'))
    action = '&action=auth&usr=' + str(config.usr) + '&company-key=' + str(config.companykey)
    pwd_action = str(salt_str) + str(pow_sha1.hexdigest()) + action  # This complete string needs SHA1
    auth_sign = hashlib.sha1()
    auth_sign.update(pwd_action.encode('utf-8'))
    sign = str(auth_sign.hexdigest())
    solar_url = config.baseURL + '?sign=' + sign + '&salt=' + str(salt_str) + action

    log.debug(solar_url)

    r = requests.get(solar_url)
    token = r.json()['dat']['token']
    secret = r.json()['dat']['secret']
    expire = r.json()['dat']['expire']
    # Convert expire to datetime when expiring
    d = datetime.now().today()
    expire = d + timedelta(seconds=expire)
    return token, secret, expire


# action = :
# queryPlantCurrentData - Returns json summary of energy generated
# queryPlantActiveOuputPowerOneDay - (Misspelled in API) Returns json data used in Shinemonitor for displaying
# today graph over generated energy
# queryDeviceDataOneDayPaging - Returns various json data, ex. energy generated now
# queryPlantDeviceDesignatedInformation - Return for example offline/online status of inverter
def build_request_url(action, salt_str, secret, token, dev_code, plant_id, pn, sn):
    if action == 'queryPlantCurrentData':
        action = '&action=queryPlantCurrentData&plantid=' + plant_id + '&par=ENERGY_TODAY,ENERGY_MONTH,ENERGY_YEAR,' \
                                                                       'ENERGY_TOTAL,ENERGY_PROCEEDS,ENERGY_CO2,' \
                                                                       'CURRENT_TEMP,CURRENT_RADIANT,BATTERY_SOC,' \
                                                                       'ENERGY_COAL,ENERGY_SO2'
    elif action == 'queryPlantActiveOuputPowerOneDay':
        action = '&action=queryPlantActiveOuputPowerOneDay&plantid=' + plant_id + '&date=' + datetime.today().strftime(
            '%Y-%m-%d') + '&i18n=en_US&lang=en_US'
    elif action == 'queryDeviceDataOneDayPaging':
        action = '&action=queryDeviceDataOneDayPaging&devaddr=1&pn=' + pn + '&devcode=' + dev_code + '&sn=' + \
                 sn + '&date=' + datetime.today().strftime('%Y-%m-%d') + '&page=0&pagesize=50&i18n=en_US&lang=en_US'
    elif action == 'queryPlantDeviceDesignatedInformation':
        action = '&action=queryPlantDeviceDesignatedInformation&plantid=' + plant_id + \
                 '&devtype=512&i18n=en_US&parameter=energy_today,energy_total&i18n=en_US&lang=en_US'

    req_action = str(salt_str) + secret + token + action
    req_sign = hashlib.sha1()
    req_sign.update(req_action.encode('utf-8'))
    sign = str(req_sign.hexdigest())
    req_url = config.baseURL + '?sign=' + sign + '&salt=' + str(salt_str) + '&token=' + token + action
    return req_url


def login(log):
    log.info("Logging in using credentials")
    token, secret, expire = gettoken(log, salt())
    return token, secret, expire


def get_energy_now(log, token, secret):
    req_url = build_request_url('queryDeviceDataOneDayPaging', str(salt), secret, token, config.devcode, config.plantId,
                                config.pn, config.sn)
    r = requests.get(req_url)
    errcode = r.json()['err']

    if errcode == 0:
        timestamp = r.json()['dat']['row'][0]['field'][1]
        energy_now = r.json()['dat']['row'][0]['field'][15]
        energy_now = int(energy_now) / 1000
        r = '{"timestamp": "' + str(timestamp) + '"'
        r += ', "voltage": ' + str(energy_now) + '}'
        return r
    else:
        log.error('{Errorcode: ' + str(errcode) + '}')


def get_energy_total(log, token, secret):
    req_url = build_request_url('queryPlantCurrentData', str(salt), secret, token, config.devcode, config.plantId,
                                config.pn, config.sn)
    r = requests.get(req_url)
    errcode = r.json()['err']

    if errcode == 0:
        # energy_today = r.json()['dat'][0]['val']
        # energy_month = r.json()['dat'][1]['val']
        # energy_year = r.json()['dat'][2]['val']
        energy_total = r.json()['dat'][3]['val']
        r = '{"value": ' + str(round(float(energy_total), 2)) + '}'
        return r
    else:
        log.error('{Errorcode: ' + str(errcode) + '}')
