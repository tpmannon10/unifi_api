import requests
import json
import os
from dotenv import load_dotenv


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
            print(json.dumps(sites, indent=4))

        # metrics = unifi_data(base_url, '/api/s/jiac21ob/stat/sta', session)
        # print(json.dumps(metrics, indent=4))
        logout_of_unifi(base_url, '/api/logout', session)
