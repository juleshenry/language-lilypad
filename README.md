# What is Language Lilypad?

In this project, we leverage Rust to make a dictionary via async API calls to a text box. The definitions are loaded as they are typed.

Furthermore, for every word in the definition, a definition is provided via hyperlink.

Hence, when using this dictionary, one may leap-frog from word to word, as if they were lilypads.

## Multi-Language Support

Language Lilypad now supports multiple languages through a robust framework:

- **Spanish (Español)** - 85,000+ words
- **Portuguese (Português)** - Ready to expand
- **French (Français)** - Ready to expand
- **Korean (한국어)** - Ready to expand

### Adding New Languages

See the [Language Framework documentation](language_framework/README.md) for details on adding new languages.

Quick start:
```bash
# List available languages
python3 language_framework/populate_database.py --list

# Populate a language dictionary
python3 language_framework/populate_database.py --language pt

# Populate all languages
python3 language_framework/populate_database.py --all
```

## Getting Started

### 1. Install Backend Dependencies

```bash
cd react_version/backend
npm install
```

### 2. Populate Language Dictionaries

Populate the backend database with your desired languages:

```bash
# From the repository root
python3 language_framework/populate_database.py --all --database react_version/backend/db/palabras.db

# Or populate individual languages
python3 language_framework/populate_database.py --language pt --database react_version/backend/db/palabras.db
python3 language_framework/populate_database.py --language fr --database react_version/backend/db/palabras.db
python3 language_framework/populate_database.py --language ko --database react_version/backend/db/palabras.db
```

### 3. Run the Servers

First, run the backend dictionary server in `react_version/backend`:

```bash
cd react_version/backend
node server.js
```

Next, run the backend translation server in `react_version`:

```bash
cd react_version
python3 translation_server.py
```

Finally, run the frontend Next server in `react_version/frontend/languagelilypad`:

```bash
cd react_version/frontend/langlilypad
npx next dev --port 3333
```

Open [http://localhost:3333](http://localhost:3333) with your browser to see the result.

## API Usage

### Query a word in a specific language

```bash
# Portuguese
curl -X POST http://localhost:3000/definir/multilang \
  -H "Content-Type: application/json" \
  -d '{"palabra": "amor", "language": "pt"}'

# French
curl -X POST http://localhost:3000/definir/multilang \
  -H "Content-Type: application/json" \
  -d '{"palabra": "amour", "language": "fr"}'

# Korean
curl -X POST http://localhost:3000/definir/multilang \
  -H "Content-Type: application/json" \
  -d '{"palabra": "사랑", "language": "ko"}'
```

### Get list of supported languages

```bash
curl http://localhost:3000/definir/multilang/languages
```

![ejemplo](language_lilypad.gif)