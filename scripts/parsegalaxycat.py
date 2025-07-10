#!/usr/bin/env python3
import requests
import csv
import sys
import json
from bs4 import BeautifulSoup
import re

def fetch_instances(url):
    try:
        print(f"Fetching data from: {url}")
        resp = requests.get(url, timeout=30, headers={'Accept': 'text/html,application/xhtml+xml'})
        resp.raise_for_status()
        
        print(f"Response status: {resp.status_code}")
        print(f"Response content type: {resp.headers.get('content-type', 'unknown')}")
        print(f"Response length: {len(resp.text)} characters")
        
        if not resp.text.strip():
            print("Error: Empty response from server")
            sys.exit(1)
        
        return resp.text
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching data: {e}")
        sys.exit(1)

def parse_html_table(html_content):
    """Parse the Galaxy Catalog HTML table and extract instance data"""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("Error: BeautifulSoup4 library not found. Please install it with:")
        print("pip3 install beautifulsoup4")
        sys.exit(1)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table with instance data
    table = soup.find('table', class_='table')
    if not table:
        print("Error: Could not find instances table in HTML")
        sys.exit(1)
    
    instances = []
    rows = table.find('tbody').find_all('tr')
    
    print(f"Found {len(rows)} instance rows in table")
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 6:  # Ensure we have all expected columns
            # Extract data from each cell
            brand = cells[0].get_text(strip=True)
            
            # URL - extract from the link
            url_link = cells[1].find('a')
            url = url_link.get('href') if url_link else ''
            # Clean up URL - remove http:// or https:// for consistency
            clean_url = url.replace('http://', '').replace('https://', '') if url else ''
            
            location = cells[2].get_text(strip=True)
            
            # Split location into region (last part after comma)
            if ', ' in location:
                region = location.split(', ')[-1]
            else:
                region = location if location != 'Unknown' else ''
            
            # Properties - check for login requirements and quotas
            properties_cell = cells[3]
            login_required = 'Login required' in str(properties_cell)
            quotas_enabled = 'Quotas enabled' in str(properties_cell)
            has_terms = properties_cell.find('a', title='Terms') is not None
            
            version = cells[4].get_text(strip=True)
            
            # Tools count - extract number from the link or text
            tools_cell = cells[5]
            tools_link = tools_cell.find('a')
            tools_count = tools_link.get_text(strip=True) if tools_link else tools_cell.get_text(strip=True)
            
            # Create institution name - use brand name or derive from URL
            institution = brand
            
            # Create notes with additional info
            notes_parts = []
            if login_required:
                notes_parts.append("Login required")
            if quotas_enabled:
                notes_parts.append("Quotas enabled")
            if has_terms:
                notes_parts.append("Has terms of service")
            if version:
                notes_parts.append(f"Galaxy v{version}")
            if tools_count and tools_count != '0':
                notes_parts.append(f"{tools_count} tools")
            
            notes = "; ".join(notes_parts)
            
            # Map to master spreadsheet columns
            instance = {
                'Name': brand,
                'URL': clean_url,
                'Region': region,
                'Institution': institution,
                'Notes': notes
            }
            instances.append(instance)
    
    return instances

def instances_to_csv(instances, out_csv):
    if not instances:
        print("No instances found to write to CSV")
        return
    
    # Define the specific column order for the master spreadsheet
    keys = ['Name', 'URL', 'Region', 'Institution', 'Notes']
    
    print(f"Writing {len(instances)} instances with fields: {keys}")
    
    try:
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for inst in instances:
                if isinstance(inst, dict):
                    row = {k: inst.get(k, '') for k in keys}
                    writer.writerow(row)
    except IOError as e:
        print(f"Error writing to file {out_csv}: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) not in (1,2,3):
        print(f"Usage: {sys.argv[0]} [instances_url] [output.csv]")
        print(f"Default URL: https://galaxycat.france-bioinformatique.fr/instances")
        sys.exit(1)
    
    # Use Galaxy Catalog as default URL
    default_url = "https://galaxycat.france-bioinformatique.fr/instances"
    
    if len(sys.argv) == 1:
        url = default_url
        out_csv = 'instances.csv'
    elif len(sys.argv) == 2:
        # Could be URL or output filename
        if sys.argv[1].endswith('.csv'):
            url = default_url
            out_csv = sys.argv[1]
        else:
            url = sys.argv[1]
            out_csv = 'instances.csv'
    else:  # len(sys.argv) == 3
        url = sys.argv[1]
        out_csv = sys.argv[2]
    print(f"Fetching from URL: {url}")
    print(f"Output file: {out_csv}")
    
    html_content = fetch_instances(url)
    instances = parse_html_table(html_content)
    
    print(f"Parsed {len(instances)} instances from HTML table")

    instances_to_csv(instances, out_csv)
    print(f"Saved {len(instances)} entries to {out_csv}")

if __name__ == "__main__":
    main()