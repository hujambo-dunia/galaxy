import requests
import jmespath
import json
import time # Track request timestamps for rate limiting
from get_server_instance import fetch_instances

# ip-api.com free tier: 45 requests per minute from an IP address (rate-limited). See https://ip-api.com/docs/
# If you exceed the limit, you will get HTTP 429 Too Many Requests.
RATE_LIMIT_LOCATION_PER_MINUTE = 45
LOG_FILE = "server.geojson"

request_timestamps = []

platform_urls = fetch_instances()

def verify_rate_limit():
    """
    Prevent exceeding ip-api.com free tier rate limit (45 requests/minute).
    Sleeps if the limit would be exceeded.
    """
    global request_timestamps
    now = time.time()
    # Remove timestamps older than 60 seconds
    request_timestamps = [t for t in request_timestamps if now - t < 60]
    if len(request_timestamps) >= RATE_LIMIT_LOCATION_PER_MINUTE:
        # Sleep until we can make another request
        sleep_time = 60 - (now - request_timestamps[0])
        print(f"Rate limit reached ({RATE_LIMIT_LOCATION_PER_MINUTE}/min). Sleeping for {sleep_time:.1f} seconds...")
        time.sleep(max(sleep_time, 0))
        # After sleep, clean up timestamps again
        now = time.time()
        request_timestamps = [t for t in request_timestamps if now - t < 60]
    # Record this request
    request_timestamps.append(time.time())

def get_server_location(platform_url):
    # Extract domain from URL
    from urllib.parse import urlparse
    domain = urlparse(platform_url).netloc
    if not domain:
        print(f"Could not parse domain from {platform_url}")
        return None
    verify_rate_limit()
    try:
        geo_resp = requests.get(f"http://ip-api.com/json/{domain}", timeout=10)
        geo_data = geo_resp.json()
        if geo_data.get('status') != 'success':
            print(f"Location lookup failed for {platform_url}: {geo_data.get('message', 'Unknown error')}")
            return None
        # Collect all required fields
        location = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [geo_data.get('lon'), geo_data.get('lat')]
            },
            "properties": {
                "city": geo_data.get('city'),
                "zipcode": geo_data.get('zip'),
                "country": geo_data.get('country'),
                "country_code": geo_data.get('countryCode'),
                "latitude": geo_data.get('lat'),
                "longitude": geo_data.get('lon'),
                "server_url": platform_url
            }
        }
        print(f"{platform_url}: {location['properties']}")
        return location
    except Exception as e:
        print(f"Error getting location for {platform_url}: {e}")
        return None

def format_log(locations):
    # Overwrite the log file with a new FeatureCollection
    geojson = {
        "type": "FeatureCollection",
        "features": locations
    }
    with open(LOG_FILE, 'w') as f:
        json.dump(geojson, f, indent=2)

if __name__ == "__main__":
    # fetch_instances()
    features = []
    for url in platform_urls:
        location = get_server_location(url)
        if location:
            features.append(location)
    format_log(features)
