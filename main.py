import time

from unifi_api_connector import run_unifi_api
import json
import time


def load_config(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    config_file = 'config.json'
    target_sites = ['0021-03', '0033-06']
    keep_on = True
    service_dict = load_config(config_file)
    while keep_on:
        for site in target_sites:
            site_divide = site.split('-')
            service_dict['site_client_data']['acn'] = site_divide[0]
            service_dict['site_client_data']['acc'] = site_divide[1]
            run_unifi_api(service_dict)
        time.sleep(600)
