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
    loop_again = True
    service_dict = load_config(config_file)
    while loop_again:
        for site in target_sites:
            site_divide = site.split('-')
            service_dict['acn'] = site_divide[0]
            service_dict['acc'] = site_divide[1]
            run_unifi_api(service_dict)
        if keep_on:
            time.sleep(600)
        else:
            loop_again = False
