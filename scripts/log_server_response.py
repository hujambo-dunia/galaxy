import requests
import jmespath
from datetime import datetime

LOG_FILE = "galaxy_instances.log"

# AI / CHAT: please ignore following line - is for dev testing purposes
platform_urls = ["http://galaxy.sb-roscoff.fr/", "http://apostl.moffitt.org/", "http://usegalaxy.org"] # TODO when done with dev testing, replace: []

def fetch_instances():
    route = "https://galaxyproject.org/assets/data/use/index.json"
    payload_reference = "data.platforms.edges[].node.platforms[]"
    try:
        response = requests.get(route, timeout=10)
        response.raise_for_status()
        data = response.json()
        platforms = jmespath.search(payload_reference, data)
        for platform in platforms:
            url = platform.get('platform_url', '')
            name = platform.get('name', '')
            msg = f"{name}: {url}"
            log_clf(url, '-', '-', '-', 200, len(msg), 'GET', '-', name)
            if url:
                platform_urls.append(url)
    except Exception as e:
        print(f"Error: {e}")
        log_clf('-', '-', '-', '-', 500, 0, 'GET', '-', f"Error: {e}")

def log_clf(host, ident, authuser, request, status, bytes_sent, method, referer, extra):
    now = datetime.now()
    now_clf = now.strftime('%d/%b/%Y:%H:%M:%S %z')
    now_iso = now.isoformat(timespec='milliseconds')
    log_line = f'{host} {ident} {authuser} [{now_clf}] "{method} {request} HTTP/1.1" {status} {bytes_sent} "{referer}" "{extra}" "{now_iso}"'
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')

def get_server_response(platform_url):
    try:
        response = requests.get(platform_url, timeout=10)
        status = response.status_code
        reason = response.reason
        content_length = len(response.content)
        log_clf(platform_url, '-', '-', platform_url, status, content_length, 'GET', '-', reason)
        print(f"{platform_url} - {status} {reason}")
    except Exception as e:
        log_clf(platform_url, '-', '-', platform_url, 500, 0, 'GET', '-', f"ERROR: {e}")
        print(f"{platform_url} - ERROR: {e}")

if __name__ == "__main__":
    fetch_instances()
    for url in platform_urls:
        get_server_response(url)
