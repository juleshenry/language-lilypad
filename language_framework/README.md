# Language Framework

This framework provides a modular system for adding new language dictionaries to Language Lilypad.

## Architecture

### Components

1. **Dictionary Scraper** (`dictionary_scraper.py`): Base class for extracting dictionary data from various sources
2. **Language Config** (`language_config.py`): Configuration management for language-specific settings
3. **Database Manager** (`database_manager.py`): Multi-language database operations
4. **Language Implementations** (`languages/`): Language-specific implementations

## Adding a New Language

1. Create a language configuration in `languages/your_language.json`
2. Implement a language-specific scraper if needed (or use generic scraper)
3. Run the scraper to populate the database
4. Update the backend to include the new language

## Supported Languages

- Spanish (existing)
- Portuguese
- French
- Korean

## Data Sources

The framework supports multiple dictionary data sources:
- PDF dictionaries (parsed with pdfplumber)
- JSON dictionaries
- API-based dictionaries
- Web scrapers (BeautifulSoup)
