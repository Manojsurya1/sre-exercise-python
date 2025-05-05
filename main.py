import yaml
import requests
import time
import sys
from collections import defaultdict
from urllib.parse import urlparse

# Load configuration from YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Perform health check with status code and latency requirement
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')

    try:
        start = time.time()
        response = requests.request(method, url, headers=headers, data=body, timeout=0.5)
        duration_ms = (time.time() - start) * 1000

        if 200 <= response.status_code < 300 and duration_ms <= 500:
            return "UP"
        return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Monitor endpoints every 15 seconds and log availability by domain (ignoring port)
def monitor_endpoints(file_path):
    print(" Monitoring started...")

    config = load_config(file_path)
    print("Loaded config:", config)

    if not config:
        print(" No endpoints found in YAML file.")
        return

    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        print(f" Starting check cycle @ {time.strftime('%Y-%m-%d %H:%M:%S')}")

        for endpoint in config:
            parsed = urlparse(endpoint["url"])
            domain = parsed.hostname
            print(f" Checking domain: {domain}, URL: {endpoint['url']}")

            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        print(f"\n Availability Report:")
        for domain, stats in domain_stats.items():
            availability = round((stats["up"] / stats["total"]) * 100, 2)
            print(f" {domain} ➜ {availability}% availability")
        print("--------------------------------------------------")
        time.sleep(15)

# Entry point
if __name__ == "__main__":
    print(" Script started")  # Confirm script is running

    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\n Monitoring stopped by user.")
