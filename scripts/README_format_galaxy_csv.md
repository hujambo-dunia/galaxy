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
The output CSV will have these columns:
- `Instance Name` - Same as Resource Name
- `URL` - Same as Server URL
- `Institution` - Summary text with embedded markdown link to Page URL
- `Keywords` - Same as original Keywords

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
- Handles CSV encoding properly (UTF-8)
- Provides detailed error messages and progress feedback
- Preserves all keywords from the original file

## Example Output
The Institution column will contain markdown-formatted links like:
```
[Analysis and bioinformatics for Marine Science.](https://galaxyproject.org/use/abims/)
```

This format allows the institution description to be clickable in markdown-aware applications while still being readable as plain text.
