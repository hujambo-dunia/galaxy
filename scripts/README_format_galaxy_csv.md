# Galaxy CSV Formatter

This script formats the `galaxyproject.use.csv` file for use with the galaxy tracker in `index.html`.

## Input Format
The input CSV should have these columns:
- `Resource Name` - The name of the Galaxy instance
- `Page URL` - Link to the Galaxy project page
- `Server URL` - Direct URL to the Galaxy server
- `Summary` - Description of the instance
- `Keywords` - Comma-separated keywords

## Output Format
The output CSV will have these columns in the exact order expected by the Galaxy Tracker spreadsheet:
- `Tier` - Empty field for manual priority assignment (1, 2, 3, etc.)
- `Name` - Same as Resource Name
- `URL` - Same as Server URL
- `Region` - Detected country/region based on Server URL
- `Institution` - Summary text with embedded markdown link to Page URL
- `Notes` - Keywords from the original data

## Usage

### Basic usage (uses default file paths):
```bash
python format_galaxy_csv.py
```

### Specify input file:
```bash
python format_galaxy_csv.py path/to/input.csv
```

### Specify both input and output files:
```bash
python format_galaxy_csv.py path/to/input.csv path/to/output.csv
```

## Default Files
- Input: `./galaxyproject.use.csv`
- Output: `./galaxy_tracker_formatted.csv`

## Features
- Automatically skips rows with missing Resource Name or Server URL
- Creates markdown links combining Summary text with Page URL
- Detects country/region from Server URL using domain analysis
- Handles CSV encoding properly (UTF-8)
- Provides detailed error messages and progress feedback
- Preserves all keywords from the original file

## Region Detection
The script analyzes server URLs to determine the geographic region/country:
- Uses domain patterns (.fr = France, .de = Germany, etc.)
- Recognizes specific institutional domains (e.g., usegalaxy.eu = Europe)
- Maps university and research institution domains to countries
- Falls back to "Unknown" for unclear domains or IP addresses

### Region Distribution Example:
- Europe: 26 instances
- International: 23 instances  
- France: 19 instances
- United States: 16 instances
- India: 11 instances
- Unknown: 6 instances
- And many others...

## Example Output
The Institution column will contain markdown-formatted links like:
```
[Analysis and bioinformatics for Marine Science.](https://galaxyproject.org/use/abims/)
```

The output format matches the Google Spreadsheet structure expected by the Galaxy Instance Tracker:
- **Tier**: Empty (ready for manual tier assignment)
- **Name**: AB-OpenLab
- **URL**: http://ab-openlab.csir.res.in/frog/
- **Region**: India  
- **Institution**: [FROG stands for...](https://galaxyproject.org/use/ab-openlab/)
- **Notes**: Genomics

This format allows the CSV to be directly imported into the Google Spreadsheet that feeds the Galaxy Instance Tracker interface.
