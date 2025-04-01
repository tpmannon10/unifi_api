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


def process_json_files(directory, metric, outfile):
    evse_metric = {}
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if data['site'] not in evse_metric.keys():
                evse_metric[data['site']] = {
                    f'evse_{metric}': {}
                }
            for item in data['wireless_client_data']:
                if item['hostname'] not in evse_metric[data['site']][f'evse_{metric}'].keys():
                    evse_metric[data['site']][f'evse_{metric}'][item['hostname']] = []
                    evse_metric[data['site']][f'evse_{metric}'][item['hostname']].append(item[metric])
                else:
                    evse_metric[data['site']][f'evse_{metric}'][item['hostname']].append(item[metric])

    for site in evse_metric.keys():
        for host in evse_metric[site][f'evse_{metric}'].keys():
            metric_sum = sum(evse_metric[site][f'evse_{metric}'][host])
            metric_avg = metric_sum/len(evse_metric[site][f'evse_{metric}'][host])
            evse_metric[site][f'evse_{metric}'][host] = metric_avg

    with open(outfile, 'w', encoding='utf-8') as file:
        json.dump(evse_metric, file, indent=4)
    return evse_metric


open_directory_path = './client_metrics/WAP_Baseline_client'
evse_data = process_json_files(open_directory_path, 'rssi', 'client_aggregate.json')

print(evse_data.keys())
print(evse_data['0021-03'].keys())
print(evse_data['0033-06'].keys())
print(evse_data['0021-03']['evse_rssi'].keys())
print(evse_data['0033-06']['evse_rssi'].keys())
