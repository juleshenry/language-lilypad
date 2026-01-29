# Database to JSON Converter

This script converts the SQLite database (`palabras.db`) into indexed JSON files for easy lookup and distribution.

## Features

- **Automatic chunking**: Splits data into multiple JSON files, each less than 25MB
- **Indexed naming**: Files are named as `first_word__last_word.json` for simple lookup
- **Sorted output**: Words are sorted alphabetically within and across files
- **UTF-8 support**: Properly handles Spanish characters and special symbols

## Usage

```bash
python3 db_to_json.py <database_path> [output_directory]
```

### Examples

Convert the database to JSON files in the current directory:
```bash
python3 db_to_json.py ../palabras.db ./json_output
```

Convert the database to JSON files in a specific directory:
```bash
python3 db_to_json.py /path/to/palabras.db /path/to/output
```

## Output Format

Each JSON file is a dictionary with words as keys and definitions as values:

```json
{
  "palabra1": "definición de palabra1",
  "palabra2": "definición de palabra2",
  ...
}
```

## File Naming

Files are named using the format: `first_word__last_word.json`

For example:
- `aardvark__banana.json` - Contains words from "aardvark" to "banana"
- `car__dog.json` - Contains words from "car" to "dog"

This naming scheme allows for:
1. **Quick lookup**: You can determine which file contains a word by comparing it alphabetically
2. **Easy distribution**: Files can be distributed separately or cached individually
3. **Human-readable**: The filename tells you exactly what's inside

## Requirements

- Python 3.6 or higher
- SQLite3 (included with Python)
- No external dependencies required

## Implementation Details

The script:
1. Connects to the SQLite database
2. Fetches all words and definitions, sorted alphabetically
3. Estimates JSON size for each entry
4. Groups words into chunks that don't exceed 25MB
5. Writes each chunk to a separate JSON file with an indexed name
6. Provides a summary of files created

## Notes

- The script automatically creates the output directory if it doesn't exist
- All JSON files use UTF-8 encoding with proper Unicode support
- The script includes safety checks to ensure no file exceeds 25MB
- Words are sorted alphabetically for consistent output
