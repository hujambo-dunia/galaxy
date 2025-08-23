import requests
from datetime import datetime
from get_server_instance import fetch_instances

LOG_FILE = "server.yml"

platform_urls = fetch_instances()

import yaml

def format_log_toolset(instance_url, tools):
    """
    Logs the instance URL and its list of tools (name and version) to the YAML log file.
    """
    entry = {"instance_url": instance_url, "tools": tools}
    with open(LOG_FILE, 'a') as f:
        yaml.dump([entry], f)

def get_server_toolset(platform_url):
    api_url = platform_url.rstrip('/') + '/api/tools'
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        tools_data = response.json()
        # Extract Name, Version, Link from nested elems[*]
        tools = []
        for tool in tools_data:
            elems = tool.get('elems', [])
            for elem in elems:
                name = elem.get('name', 'unknown')
                version = elem.get('version', 'unknown')
                link = elem.get('link', 'unknown')
                tools.append({
                    'name': name,
                    'version': version,
                    'link': link
                })
        format_log_toolset(platform_url, tools)
        print(f"{platform_url}: {len(tools)} tools logged.")
    except Exception as e:
        print(f"{platform_url} - ERROR: {e}")

if __name__ == "__main__":
    # fetch_instances()
    for url in platform_urls:
        get_server_toolset(url)
