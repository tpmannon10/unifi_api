from unifi_api_connector import run_unifi_api


if __name__ == '__main__':
    service_dict = {
        "site_id_update": True
    }
    run_unifi_api(service_dict)
