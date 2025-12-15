# Language Framework Usage Guide

## Overview

The Language Framework provides a modular system for adding dictionary support for multiple languages to Language Lilypad. This guide explains how to use the framework to add new languages and work with existing ones.

## Quick Start

### 1. List Available Languages

```bash
python3 language_framework/populate_database.py --list
```

### 2. Populate a Language Dictionary

```bash
# Populate Portuguese dictionary
python3 language_framework/populate_database.py --language pt

# Populate French dictionary
python3 language_framework/populate_database.py --language fr

# Populate Korean dictionary
python3 language_framework/populate_database.py --language ko
```

### 3. Populate All Languages

```bash
python3 language_framework/populate_database.py --all
```

### 4. Check Database Statistics

```bash
python3 language_framework/populate_database.py --stats
```

## Adding a New Language

To add a new language to the framework, follow these steps:

### Step 1: Create Language Configuration

Create a JSON configuration file in `language_framework/languages/` named `{language_code}.json`:

```json
{
  "name": "Language Name",
  "native_name": "Native Language Name",
  "language_code": "xx",
  "database_table": "xx_words",
  "enabled": true,
  "source_type": "json",
  "source_config": {
    "json_path": "language_framework/data/xx_dictionary.json",
    "word_key": "word",
    "definition_key": "definition"
  },
  "parser_config": {
    "tokenize_pattern": "[\\w'-]+",
    "clean_patterns": ["\\(.*?\\)", "\\[.*?\\]"]
  }
}
```

### Step 2: Prepare Dictionary Data

#### Option A: JSON Dictionary

Create a JSON file in `language_framework/data/` with your dictionary data:

```json
[
  {
    "word": "hello",
    "definition": "A greeting used when meeting someone"
  },
  {
    "word": "world",
    "definition": "The earth, together with all its countries and peoples"
  }
]
```

#### Option B: PDF Dictionary

If you have a PDF dictionary:

1. Place the PDF in an appropriate location (e.g., `src_langz/`)
2. Update the language configuration with PDF settings:

```json
{
  "source_type": "pdf",
  "source_config": {
    "pdf_path": "src_langz/your_dictionary.pdf",
    "start_page": 1,
    "end_page": 100,
    "pattern": "your-regex-pattern"
  }
}
```

#### Option C: API Dictionary

For API-based dictionaries:

```json
{
  "source_type": "api",
  "source_config": {
    "api_url": "https://api.example.com/dictionary",
    "word_key": "word",
    "definition_key": "definition",
    "headers": {},
    "params": {}
  }
}
```

### Step 3: Populate the Database

```bash
python3 language_framework/populate_database.py --language xx
```

### Step 4: Update Backend Routes

The multi-language route (`/definir/multilang`) automatically supports new languages if they're added to the `LANGUAGE_TABLES` configuration in `react_version/backend/src/routes/definir_multilang.js`:

```javascript
const LANGUAGE_TABLES = {
  es: "palabras",
  pt: "pt_words",
  fr: "fr_words",
  ko: "ko_words",
  xx: "xx_words",  // Add your new language here
};
```

### Step 5: Update Frontend (Optional)

Update the language selector in the frontend to include the new language.

## Using the Backend API

### Query a Word in a Specific Language

**Endpoint:** `POST /definir/multilang`

**Request Body:**
```json
{
  "palabra": "amor",
  "language": "pt"
}
```

**Response:**
```json
{
  "palabra": "amor",
  "definicion": "Sentimento intenso de afeição, carinho e dedicação...",
  "palabras": {
    "sentimento": "...",
    "afeição": "..."
  },
  "language": "pt"
}
```

### Get Supported Languages

**Endpoint:** `GET /definir/multilang/languages`

**Response:**
```json
[
  { "code": "es", "name": "Spanish", "nativeName": "Español" },
  { "code": "pt", "name": "Portuguese", "nativeName": "Português" },
  { "code": "fr", "name": "French", "nativeName": "Français" },
  { "code": "ko", "name": "Korean", "nativeName": "한국어" }
]
```

## Python API

### Using the Framework Programmatically

```python
from language_framework.language_config import LanguageConfig, LanguageRegistry
from language_framework.dictionary_scraper import get_scraper
from language_framework.database_manager import DatabaseManager

# Load language configuration
config = LanguageConfig('pt')

# Create scraper
scraper = get_scraper(
    language_code='pt',
    source_type=config.source_type,
    config=config.source_config
)

# Scrape dictionary
words = scraper.scrape()

# Populate database
with DatabaseManager() as db:
    db.create_language_table('pt', 'pt_words')
    db.insert_words('pt', words, 'pt_words')
```

### Query Words from Python

```python
from language_framework.database_manager import DatabaseManager

with DatabaseManager() as db:
    result = db.query_word('pt', 'amor')
    if result:
        print(f"Word: {result['palabra']}")
        print(f"Definition: {result['definicion']}")
```

## Architecture

### Framework Components

1. **Language Config** (`language_config.py`): Manages language-specific settings
2. **Dictionary Scraper** (`dictionary_scraper.py`): Extracts dictionary data from various sources
3. **Database Manager** (`database_manager.py`): Handles multi-language database operations
4. **Population Tool** (`populate_database.py`): CLI tool for database population

### Supported Source Types

- **JSON**: Simple JSON files with word-definition pairs
- **PDF**: PDF dictionaries with pattern-based extraction
- **API**: REST API endpoints that provide dictionary data
- **Custom**: Extend `DictionaryScraper` for custom sources

## Best Practices

1. **Dictionary Quality**: Start with at least 100-1000 common words for a useful dictionary
2. **Definition Format**: Keep definitions concise and clear
3. **Encoding**: Always use UTF-8 encoding for dictionary files
4. **Testing**: Test with a small dataset before importing large dictionaries
5. **Backups**: Backup your database before adding new languages

## Troubleshooting

### "Configuration file not found" error
- Ensure the language configuration file exists in `language_framework/languages/`
- Check that the filename matches the language code (e.g., `pt.json` for Portuguese)

### "JSON file not found" error
- Verify the `json_path` in your language configuration
- Ensure the path is relative to the repository root

### Words not appearing in queries
- Check that the table was created: `python3 language_framework/populate_database.py --stats`
- Verify the `database_table` setting in your language configuration
- Ensure the backend route includes your language in `LANGUAGE_TABLES`

### PDF parsing issues
- Adjust the `pattern` in your configuration to match your PDF structure
- Consider implementing a custom parser by extending `PDFDictionaryScraper`

## Examples

### Example 1: Portuguese Dictionary Query

```bash
# Populate Portuguese dictionary
python3 language_framework/populate_database.py --language pt

# Query using curl
curl -X POST http://localhost:3000/definir/multilang \
  -H "Content-Type: application/json" \
  -d '{"palabra": "amor", "language": "pt"}'
```

### Example 2: Add a Small Test Dictionary

```bash
# Create configuration
cat > language_framework/languages/test.json << 'EOF'
{
  "name": "Test",
  "native_name": "Test",
  "language_code": "test",
  "database_table": "test_words",
  "enabled": true,
  "source_type": "json",
  "source_config": {
    "json_path": "language_framework/data/test_dictionary.json"
  }
}
EOF

# Create dictionary data
cat > language_framework/data/test_dictionary.json << 'EOF'
[
  {"word": "test", "definition": "A procedure for testing something"},
  {"word": "example", "definition": "A thing characteristic of its kind"}
]
EOF

# Populate
python3 language_framework/populate_database.py --language test
```

## Contributing

To contribute new languages or improvements to the framework:

1. Follow the steps above to add your language
2. Test thoroughly with sample queries
3. Document any special requirements or parsing logic
4. Submit a pull request with your changes

## License

Same as the Language Lilypad project.
