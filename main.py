from unifi_api_connector import run_unifi_api


if __name__ == '__main__':
    service_dict = {
        "site_id_update": False,
        "site_client_data": {
            "get_client_data": True,
            "acn": "0021",
            "acc": "03",
            "metrics": [
                "ap_mac",
                "oui",
                "last_ip",
                "first_seen",
                "last_seen",
                "disconnect_timestamp",
                "last_uplink_mac",
                "mac",
                "hostname",
                "_uptime_by_uap",
                "_last_seen_by_uap",
                "ip",
                "channel",
                "essid",
                "noise",
                "nss",
                "rx_rate",
                "rssi",
                "signal",
                "tx_mcs",
                "tx_power",
                "tx_rate",
                "tx_retry_burst_count",
                "uptime",
                "tx_bytes",
                "rx_bytes",
                "tx_packets",
                "rx_packets",
                "bytes-r",
                "tx_bytes-r",
                "rx_bytes-r",
                "tx_retries",
                "wifi_tx_attempts",
                "wifi_tx_dropped",
                "wifi_tx_retries_percentage"
            ]
        }
    }
    run_unifi_api(service_dict)
