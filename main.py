import time

from unifi_api_connector import run_unifi_api
import json
import time


def load_config(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    config_files = ['config.json', 'config2.json']
    keep_on = True
    while keep_on:
        for setting in config_files:
            service_dict = load_config(setting)
            run_unifi_api(service_dict)
        time.sleep(600)
