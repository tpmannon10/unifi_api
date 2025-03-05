import json


def load_config(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data


config_file = '0033-06_syslog_2-14_2-28-2025.json'
service_dict = load_config(config_file)

event_keys = []
for item in service_dict["data"]:
    if item["key"]:
        if item["key"] not in event_keys:
            event_keys.append(item["key"])

print(event_keys)
