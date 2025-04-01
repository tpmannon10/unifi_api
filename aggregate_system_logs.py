import os
import json
from datetime import datetime, timedelta


def correct_timestamp(timestamp):
    try:
        dt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        corrected_dt = dt + timedelta(hours=7)
        return corrected_dt.strftime('%Y-%m-%dT%H:%M:%S')
    except ValueError as e:
        print(f"Error parsing timestamp: {e}")
        return timestamp


def process_json_file(directory, metric, outfile):
    evse_metric = {}
    with open(directory, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if data['site'] not in evse_metric.keys():
        evse_metric[data['site']] = {
            f'evse_{metric}': {}
        }
    for item in data['site_events']:
        if item['key'] == metric:
            if item['user'] not in evse_metric[data['site']][f'evse_{metric}'].keys():
                evse_metric[data['site']][f'evse_{metric}'][item['user']] = 0
                evse_metric[data['site']][f'evse_{metric}'][item['user']] += 1
            else:
                evse_metric[data['site']][f'evse_{metric}'][item['user']] += 1

    with open(outfile, 'w', encoding='utf-8') as file:
        json.dump(evse_metric, file, indent=4)
    return evse_metric


open_directory_path = './system_logs/WAP_Baseline_logs/0033-06_syslog_all_device_events_2025-03-10T09_12_28.json'
evse_data = process_json_file(open_directory_path, 'EVT_WU_Disconnected', 'syslog_aggregate.json')
