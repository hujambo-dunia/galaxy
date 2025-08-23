import json
import yaml
import os
from flask import Flask, jsonify

app = Flask(__name__)

def fetch_instances():
	"""
	Fetches Galaxy platform URLs from the Galaxy Project API.
	Returns a list of platform URLs.
	"""
	# route = "https://galaxyproject.org/assets/data/use/index.json"
	# payload_reference = "data.platforms.edges[].node.platforms[]"
	# platform_urls = []
	platform_urls = [
		"http://galaxy.sb-roscoff.fr/",
		"http://apostl.moffitt.org/",
		"http://usegalaxy.org"
	]
	# try:
	#     response = requests.get(route, timeout=10)
	#     response.raise_for_status()
	#     data = response.json()
	#     platforms = jmespath.search(payload_reference, data)
	#     for platform in platforms:
	#         url = platform.get('platform_url', '')
	#         if url:
	#             platform_urls.append(url)
	# except Exception as e:
	#     print(f"Error fetching instances: {e}")
	return platform_urls

def get_instances_info():
	"""
	Reads and merges server.log, server.geojson, and server_toolset.yml by Server URL.
	Returns merged info as a JSON object (list of dicts).
	"""
	# Read server.log
	log_path = os.path.join(os.path.dirname(__file__), '../server.log')
	geojson_path = os.path.join(os.path.dirname(__file__), '../server.geojson')
	toolset_path = os.path.join(os.path.dirname(__file__), '../server_toolset.yml')

	# Parse server.log
	server_log = {}
	try:
		with open(log_path) as f:
			for line in f:
				# Parse CLF log line
				parts = line.strip().split(' ')
				if len(parts) < 1:
					continue
				url = parts[0]
				server_log[url] = {'log_line': line.strip()}
	except Exception as e:
		print(f"Error reading server.log: {e}")

	# Parse server.geojson
	geojson = {}
	try:
		with open(geojson_path) as f:
			data = json.load(f)
			for feature in data.get('features', []):
				url = feature.get('properties', {}).get('server_url')
				if url:
					geojson[url] = feature.get('properties', {})
	except Exception as e:
		print(f"Error reading server.geojson: {e}")

	# Parse server_toolset.yml
	toolset = {}
	try:
		with open(toolset_path) as f:
			entries = yaml.safe_load(f)
			if entries:
				for entry in entries:
					url = entry.get('instance_url')
					if url:
						toolset[url] = entry.get('tools', [])
	except Exception as e:
		print(f"Error reading server_toolset.yml: {e}")

	# Merge by Server URL
	all_urls = set(server_log.keys()) | set(geojson.keys()) | set(toolset.keys())
	merged = []
	for url in all_urls:
		merged.append({
			'server_url': url,
			'log': server_log.get(url),
			'location': geojson.get(url),
			'tools': toolset.get(url)
		})
	return merged

def api_instances_info():
    data = get_instances_info()
    return jsonify(data)

app.add_url_rule('/instances_info', 'api_instances_info', api_instances_info, methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True)
