#!/usr/bin/env python3
"""
Script to format galaxyproject.use.csv for the galaxy tracker in index.html.

Input: galaxyproject.use.csv with columns:
- Resource Name, Page URL, Server URL, Summary, Keywords

Output: Formatted CSV with columns:
- Instance Name (Resource Name)
- URL (Server URL)
- Institution (Summary with embedded markdown link to Page URL)
- Keywords
"""

import csv
import sys
import os

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
                
                # Create formatted row
                formatted_row = {
                    'Instance Name': resource_name,
                    'URL': server_url,
                    'Institution': institution,
                    'Keywords': keywords
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
                fieldnames = ['Instance Name', 'URL', 'Institution', 'Keywords']
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
