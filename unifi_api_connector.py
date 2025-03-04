import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime


def login_to_unifi(base_url, credentials):
    headers = {"Content-Type": "application/json"}
    session = requests.Session()

    try:
        # Send the login request
        response = session.post(f'{base_url}/api/login', json=credentials, headers=headers, verify=False)
        response.raise_for_status()
        print("Login successful!")
        return session
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def logout_of_unifi(base, logout, sess):
    # Create a session to persist the login
    try:
        response = sess.post(f'{base}{logout}', verify=False)
        response.raise_for_status()
        print("Logout successful!")
        return
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def unifi_data(base, path, sess):
    try:
        response = sess.get(f'{base}{path}', verify=False)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while accessing the API: {e}")


def pull_site_ids(site_info_dict):
    site_names = {}
    for site in site_info_dict["data"]:
        site_names[site["desc"]] = site["name"]
    filename = 'unifi_site_list.json'
    with open(filename, 'w') as json_file:
        json.dump(site_names, json_file, indent=4)
    return


def acn_acc_string(string_dict):
    return f'{string_dict["acn"]}-{string_dict["acc"]}'


def site_id_by_acn_acc(acn_string, site_list):
    site = ""
    for key in site_list.keys():
        if acn_string in key:
            site = site_list[key]
    return site


def targeted_metrics(acn_string, metrics_list, metrics_data):
    client_metrics = []
    for client in metrics_data:
        client_data = {}
        if not client["is_wired"]:
            for metric in metrics_list:
                client_data[metric] = client[metric]
            client_metrics.append(client_data)
    client_metric_dict = {"site": acn_string, "wireless_client_data": client_metrics}
    payload_file(client_metric_dict, f'/client_metrics/{acn_string}_', 'wireless_clients_')
    return


def payload_file(payload, out_file_name, out_file_metric):
    payload["date_time"] = str(datetime.now().isoformat(timespec='seconds'))
    payload["metric"] = out_file_metric
    file_date = payload["date_time"].replace(":", "_")
    filename = os.getcwd() + out_file_name + out_file_metric + file_date + '.json'
    json_object = json.dumps(payload, indent=4)
    with open(filename, 'w') as outfile:
        outfile.write(json_object)
    return


def run_unifi_api(service):
    load_dotenv('secrets.env')
    base_url = 'https://unifi.prd.powerflex.io:443'
    credentials = {
        "username": os.getenv('UNIFI_USERNAME'),
        "password": os.getenv('UNIFI_PW'),
        "remember": os.getenv('REMEMBER')
    }

    session = login_to_unifi(base_url, credentials)

    if session:
        if service['site_id_update']:
            sites = unifi_data(base_url, '/api/self/sites', session)
            pull_site_ids(sites)
        file_name = 'unifi_site_list.json'  # Replace with your file name
        with open(file_name, 'r') as json_file:
            site_list = json.load(json_file)
        if service['site_client_data']['get_client_data']:
            acn_acc = acn_acc_string(service['site_client_data'])
            site_id = site_id_by_acn_acc(acn_acc, site_list)
            metrics_path = f'/api/s/{site_id}/stat/sta'
            metrics_full = unifi_data(base_url, metrics_path, session)
            targeted_metrics(acn_acc, service['site_client_data']['metrics'], metrics_full['data'])

        # metrics = unifi_data(base_url, '/api/s/jiac21ob/stat/sta', session)
        # print(json.dumps(metrics, indent=4))
        logout_of_unifi(base_url, '/api/logout', session)
