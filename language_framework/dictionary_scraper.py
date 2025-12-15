"""
Dictionary Scraper Framework
Base classes for extracting dictionary data from various sources
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
import sqlite3
import json
from pathlib import Path


class Word:
    """Represents a word and its definition(s)"""
    
    def __init__(self, word: str, definition: str, metadata: Optional[Dict] = None):
        """
        Initialize a Word entry
        
        Args:
            word: The word/term
            definition: The definition text
            metadata: Optional metadata (part of speech, etymology, etc.)
        """
        self.word = word.strip()
        self.definition = definition.strip()
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "word": self.word,
            "definition": self.definition,
            "metadata": self.metadata
        }


class DictionaryScraper(ABC):
    """Base class for dictionary scrapers"""
    
    def __init__(self, language_code: str, config: Dict):
        """
        Initialize the scraper
        
        Args:
            language_code: ISO language code (e.g., 'es', 'pt', 'fr', 'ko')
            config: Configuration dictionary for the scraper
        """
        self.language_code = language_code
        self.config = config
        self.words: List[Word] = []
    
    @abstractmethod
    def scrape(self) -> List[Word]:
        """
        Scrape the dictionary data
        
        Returns:
            List of Word objects
        """
        pass
    
    def parse_definition(self, raw_definition: str) -> str:
        """
        Parse and clean a raw definition string
        Can be overridden for language-specific parsing
        
        Args:
            raw_definition: Raw definition text
            
        Returns:
            Cleaned definition text
        """
        return raw_definition.strip()
    
    def validate_word(self, word: Word) -> bool:
        """
        Validate a word entry
        
        Args:
            word: Word object to validate
            
        Returns:
            True if valid, False otherwise
        """
        return bool(word.word and word.definition)
    
    def get_words(self) -> List[Word]:
        """Get the scraped words"""
        return self.words


class JSONDictionaryScraper(DictionaryScraper):
    """Scraper for JSON-based dictionaries"""
    
    def scrape(self) -> List[Word]:
        """Scrape dictionary from JSON file"""
        json_path = self.config.get("json_path")
        if not json_path:
            raise ValueError("json_path not specified in config")
        
        json_file = Path(json_path)
        if not json_file.exists():
            raise FileNotFoundError(f"JSON file not found: {json_file}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Support different JSON structures
        word_key = self.config.get("word_key", "word")
        definition_key = self.config.get("definition_key", "definition")
        
        if isinstance(data, list):
            # Array of word objects
            for entry in data:
                if isinstance(entry, dict):
                    word = entry.get(word_key)
                    definition = entry.get(definition_key)
                    if word and definition:
                        self.words.append(Word(word, definition))
        elif isinstance(data, dict):
            # Dictionary mapping words to definitions
            for word, definition in data.items():
                if isinstance(definition, str):
                    self.words.append(Word(word, definition))
                elif isinstance(definition, dict):
                    # Definition might be in a nested object
                    def_text = definition.get(definition_key, str(definition))
                    self.words.append(Word(word, def_text))
        
        return self.words


class PDFDictionaryScraper(DictionaryScraper):
    """Scraper for PDF-based dictionaries"""
    
    def scrape(self) -> List[Word]:
        """Scrape dictionary from PDF file"""
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("pdfplumber is required for PDF scraping. Install with: pip install pdfplumber")
        
        pdf_path = self.config.get("pdf_path")
        if not pdf_path:
            raise ValueError("pdf_path not specified in config")
        
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_file}")
        
        start_page = self.config.get("start_page", 1)
        end_page = self.config.get("end_page", None)
        pattern = self.config.get("pattern", None)
        
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            end = end_page if end_page else len(pdf.pages)
            for page_num in range(start_page - 1, end):
                page = pdf.pages[page_num]
                text += page.extract_text()
        
        # Parse the text using the pattern if provided
        if pattern:
            import re
            # Custom pattern-based parsing
            matches = re.findall(pattern, text, re.MULTILINE)
            for match in matches:
                if len(match) >= 2:
                    word, definition = match[0], match[1]
                    self.words.append(Word(word, definition))
        else:
            # Default parsing (can be overridden)
            self.words = self._parse_pdf_text(text)
        
        return self.words
    
    def _parse_pdf_text(self, text: str) -> List[Word]:
        """
        Default PDF text parsing
        Override for language-specific parsing
        """
        # Simple line-based parsing
        words = []
        lines = text.split('\n')
        current_word = None
        current_def = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Simple heuristic: if line starts with lowercase or is short, it's likely a definition continuation
            # Otherwise, it's a new word
            if line[0].isupper() and len(line) < 50 and not current_def:
                if current_word:
                    words.append(Word(current_word, ' '.join(current_def)))
                current_word = line
                current_def = []
            else:
                current_def.append(line)
        
        # Add the last word
        if current_word and current_def:
            words.append(Word(current_word, ' '.join(current_def)))
        
        return words


class APIDictionaryScraper(DictionaryScraper):
    """Scraper for API-based dictionaries"""
    
    def scrape(self) -> List[Word]:
        """Scrape dictionary from API"""
        try:
            import requests
        except ImportError:
            raise ImportError("requests is required for API scraping. Install with: pip install requests")
        
        api_url = self.config.get("api_url")
        if not api_url:
            raise ValueError("api_url not specified in config")
        
        headers = self.config.get("headers", {})
        params = self.config.get("params", {})
        
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse response based on config
        word_key = self.config.get("word_key", "word")
        definition_key = self.config.get("definition_key", "definition")
        data_key = self.config.get("data_key", None)
        
        if data_key:
            data = data.get(data_key, [])
        
        if isinstance(data, list):
            for entry in data:
                word = entry.get(word_key)
                definition = entry.get(definition_key)
                if word and definition:
                    self.words.append(Word(word, definition))
        
        return self.words


def get_scraper(language_code: str, source_type: str, config: Dict) -> DictionaryScraper:
    """
    Factory function to get the appropriate scraper
    
    Args:
        language_code: ISO language code
        source_type: Type of source (json, pdf, api, web)
        config: Scraper configuration
        
    Returns:
        Appropriate DictionaryScraper instance
    """
    scrapers = {
        "json": JSONDictionaryScraper,
        "pdf": PDFDictionaryScraper,
        "api": APIDictionaryScraper,
    }
    
    scraper_class = scrapers.get(source_type)
    if not scraper_class:
        raise ValueError(f"Unsupported source type: {source_type}")
    
    return scraper_class(language_code, config)
