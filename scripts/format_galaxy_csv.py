#!/usr/bin/env python3
"""
Script to format galaxyproject.use.csv for the galaxy tracker in index.html.

Input: galaxyproject.use.csv with columns:
- Resource Name, Page URL, Server URL, Summary, Keywords

Output: Formatted CSV with columns:
- Tier (empty - can be filled manually in spreadsheet)
- Name (Resource Name)
- URL (Server URL)
- Region (detected from Server URL)
- Institution (Summary with embedded markdown link to Page URL)
- Notes (Keywords from original data)
"""

import csv
import sys
import os
import re
from urllib.parse import urlparse

def detect_region_from_url(url):
    """
    Detect the country/region from a server URL.
    
    Args:
        url (str): The server URL
        
    Returns:
        str: The detected country/region or "Unknown"
    """
    if not url:
        return "Unknown"
    
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Country-specific domain mappings
        country_mappings = {
            # Specific domain patterns (checked first)
            'usegalaxy.eu': 'Europe',
            'usegalaxy.org.au': 'Australia',
            'usegalaxy.org': 'United States',
            'usegalaxy.be': 'Belgium',
            'usegalaxy.cz': 'Czech Republic',
            'usegalaxy.fr': 'France',
            'usegalaxy.no': 'Norway',
            'africa.usegalaxy.eu': 'Africa',
            'india.usegalaxy.eu': 'India',
            'erasmusmc.usegalaxy.eu': 'Netherlands',
            
            # AWS and cloud providers
            'aws': 'United States',
            'amazonaws.com': 'United States',
            
            # University and research domains
            'uni-': 'Germany',
            'inra.fr': 'France',
            'pasteur.fr': 'France',
            'sb-roscoff.fr': 'France',
            'uga.edu': 'United States',
            'tamu.edu': 'United States',
            'harvard.edu': 'United States',
            'cmu.edu': 'United States',
            'princeton.edu': 'United States',
            'umn.edu': 'United States',
            'uci.edu': 'United States',
            'ugent.be': 'Belgium',
            'csir.res.in': 'India',
            'rcees.ac.cn': 'China',
            'hku.hk': 'Hong Kong',
            'eurac.eu': 'Italy',
            'ba.infn.it': 'Italy',
            'iss.it': 'Italy',
            'angers.inra.fr': 'France',
            'embl.de': 'Germany',
            'nwafu.edu.cn': 'China',
            'genap.ca': 'Canada',
            'qmul.ac.uk': 'United Kingdom',
            'galaxyproject.org': 'United States',
            'science.psu.edu': 'United States',
            'moffitt.org': 'United States',
            'systemsbiology.nl': 'Netherlands',
            'uio.no': 'Norway',
            'ilifu.ac.za': 'South Africa',
            'excellenceinbreeding.org': 'International',
            'fi.muni.cz': 'Czech Republic',
            'u-bordeaux2.fr': 'France',
            'biochemistry.gwu.edu': 'United States',
            'nasa.gov': 'United States',
            'moralab.science': 'International',
            'hardwoodgenomics.org': 'United States',
            'networkanalyst.ca': 'Canada',
            'ipk-gatersleben.de': 'Germany',
            'morganlangille.com': 'Canada',
            'ul.edu.lb': 'Lebanon',
            'cs.ucy.ac.cy': 'Cyprus',
            'mcgill.ca': 'Canada',
            'engr.uconn.edu': 'United States',
            'disco.unimib.it': 'Italy',
            'informatik.uni-halle.de': 'Germany',
            'migale.inra.fr': 'France',
            'uni-freiburg.de': 'Germany',
            'sorbonne-universite.fr': 'France',
            'osdd.net': 'India',
            'ls.manchester.ac.uk': 'United Kingdom',
            'e-nios.com': 'International',
            'bio.di.uminho.pt': 'Portugal',
            'plantgenie.org': 'International',
            'case.edu': 'United States',
            'proteore.org': 'France',
            'protologger.de': 'Germany',
            'cerit-sc.cz': 'Czech Republic',
            'ucc.ie': 'Ireland',
            'irri.org': 'Philippines',
            'sciensano.be': 'Belgium',
            'sb-roscoff.fr': 'France',
            'uni.lu': 'Luxembourg',
            'cam.uchc.edu': 'United States',
            'hsanmartino.it': 'Italy',
            'bio.ku.dk': 'Denmark',
            'beaconlab.it': 'Italy',
            'anses.fr': 'France',
            'viramp.com': 'International',
            'life2cloud.com': 'International',
            'anvilproject.org': 'United States',
            'climb.ac.uk': 'United Kingdom',
            'globusgenomics.org': 'United States',
            'cloud.ba.infn.it': 'Italy',
            'nectar.org.au': 'Australia',
            'phenomenal-h2020.eu': 'Europe',
            'cloud.snic.se': 'Sweden',
            'surf.nl': 'Netherlands',
            'terra.bio': 'United States',
            'veupathdb.org': 'United States',
        }
        
        # Check for exact domain matches first
        for pattern, country in country_mappings.items():
            if pattern in domain:
                return country
        
        # Check for TLD patterns only if no specific match found
        tld_mappings = {
            '.au': 'Australia',
            '.be': 'Belgium', 
            '.ca': 'Canada',
            '.cz': 'Czech Republic',
            '.de': 'Germany',
            '.eu': 'Europe',
            '.fr': 'France',
            '.in': 'India',
            '.it': 'Italy',
            '.nl': 'Netherlands',
            '.no': 'Norway',
            '.org': 'International',
            '.uk': 'United Kingdom',
            '.edu': 'United States',
            '.gov': 'United States',
        }
        
        for tld, country in tld_mappings.items():
            if domain.endswith(tld):
                return country
                
        # Special cases for IP addresses or unclear domains
        if re.match(r'^\d+\.\d+\.\d+\.\d+', domain):
            return "Unknown"
            
    except Exception:
        pass
    
    return "Unknown"


def format_galaxy_csv(input_file, output_file):
    """
    Format the galaxy CSV file for the tracker.
    
    Args:
        input_file (str): Path to the input galaxyproject.use.csv file
        output_file (str): Path to the output formatted CSV file
    """
    
    formatted_rows = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            for row in reader:
                # Extract data from original CSV
                resource_name = row.get('Resource Name', '').strip()
                page_url = row.get('Page URL', '').strip()
                server_url = row.get('Server URL', '').strip()
                summary = row.get('Summary', '').strip()
                keywords = row.get('Keywords', '').strip()
                
                # Skip rows with empty resource names or server URLs
                if not resource_name or not server_url:
                    continue
                
                # Create markdown link for institution (summary with link to page URL)
                if page_url and summary:
                    institution = f"[{summary}]({page_url})"
                elif summary:
                    institution = summary
                else:
                    institution = ""
                
                # Detect region from server URL
                region = detect_region_from_url(server_url)
                
                # Create formatted row with columns in the exact order expected by the Google Spreadsheet
                formatted_row = {
                    'Tier': '',  # Empty for now - can be filled in manually in the spreadsheet
                    'Name': resource_name,
                    'URL': server_url,
                    'Region': region,
                    'Institution': institution,
                    'Notes': keywords  # Put keywords in Notes field for additional info
                }
                
                formatted_rows.append(formatted_row)
    
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return False
    except Exception as e:
        print(f"Error reading input file: {e}")
        return False
    
    # Write the formatted CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            if formatted_rows:
                fieldnames = ['Tier', 'Name', 'URL', 'Region', 'Institution', 'Notes']
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write data rows
                for row in formatted_rows:
                    writer.writerow(row)
                
                print(f"Successfully formatted {len(formatted_rows)} rows.")
                print(f"Output written to: {output_file}")
                return True
            else:
                print("No valid data found to format.")
                return False
                
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False

def main():
    """Main function to handle command line arguments and run the formatting."""
    
    # Default file paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_input = os.path.join(script_dir, 'galaxyproject.use.csv')
    default_output = os.path.join(script_dir, 'galaxy_tracker_formatted.csv')
    
    # Handle command line arguments
    if len(sys.argv) == 1:
        # No arguments - use defaults
        input_file = default_input
        output_file = default_output
    elif len(sys.argv) == 2:
        # One argument - input file specified
        input_file = sys.argv[1]
        output_file = default_output
    elif len(sys.argv) == 3:
        # Two arguments - both input and output specified
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    else:
        print("Usage: python format_galaxy_csv.py [input_file] [output_file]")
        print("  input_file: Path to galaxyproject.use.csv (default: ./galaxyproject.use.csv)")
        print("  output_file: Path to output CSV (default: ./galaxy_tracker_formatted.csv)")
        sys.exit(1)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    print(f"Input file: {input_file}")
    print(f"Output file: {output_file}")
    print("Formatting CSV...")
    
    # Run the formatting
    success = format_galaxy_csv(input_file, output_file)
    
    if success:
        print("CSV formatting completed successfully!")
        sys.exit(0)
    else:
        print("CSV formatting failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
