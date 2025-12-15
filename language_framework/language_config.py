"""
Language Configuration Management
Handles language-specific settings and configurations
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List


class LanguageConfig:
    """Configuration for a specific language dictionary"""
    
    def __init__(self, language_code: str, config_data: Optional[Dict] = None):
        """
        Initialize language configuration
        
        Args:
            language_code: ISO language code (e.g., 'es', 'pt', 'fr', 'ko')
            config_data: Configuration dictionary, or None to load from file
        """
        self.language_code = language_code
        
        if config_data:
            self.data = config_data
        else:
            self.data = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        config_dir = Path(__file__).parent / "languages"
        config_file = config_dir / f"{self.language_code}.json"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @property
    def name(self) -> str:
        """Get the language name"""
        return self.data.get("name", "")
    
    @property
    def native_name(self) -> str:
        """Get the language name in its native form"""
        return self.data.get("native_name", self.name)
    
    @property
    def database_table(self) -> str:
        """Get the database table name for this language"""
        return self.data.get("database_table", f"{self.language_code}_words")
    
    @property
    def source_type(self) -> str:
        """Get the dictionary source type (pdf, json, api, web)"""
        return self.data.get("source_type", "json")
    
    @property
    def source_config(self) -> Dict:
        """Get source-specific configuration"""
        return self.data.get("source_config", {})
    
    @property
    def parser_config(self) -> Dict:
        """Get parser-specific configuration"""
        return self.data.get("parser_config", {})
    
    @property
    def enabled(self) -> bool:
        """Check if this language is enabled"""
        return self.data.get("enabled", True)
    
    def save(self) -> None:
        """Save configuration to JSON file"""
        config_dir = Path(__file__).parent / "languages"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / f"{self.language_code}.json"
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)


class LanguageRegistry:
    """Registry of all available language configurations"""
    
    def __init__(self):
        self.languages: Dict[str, LanguageConfig] = {}
        self._load_all_configs()
    
    def _load_all_configs(self) -> None:
        """Load all language configurations from the languages directory"""
        config_dir = Path(__file__).parent / "languages"
        if not config_dir.exists():
            return
        
        for config_file in config_dir.glob("*.json"):
            language_code = config_file.stem
            try:
                self.languages[language_code] = LanguageConfig(language_code)
            except Exception as e:
                print(f"Warning: Failed to load config for {language_code}: {e}")
    
    def get(self, language_code: str) -> Optional[LanguageConfig]:
        """Get configuration for a specific language"""
        return self.languages.get(language_code)
    
    def list_enabled(self) -> List[str]:
        """List all enabled language codes"""
        return [code for code, config in self.languages.items() if config.enabled]
    
    def list_all(self) -> List[str]:
        """List all available language codes"""
        return list(self.languages.keys())
    
    def register(self, language_code: str, config_data: Dict) -> None:
        """Register a new language configuration"""
        config = LanguageConfig(language_code, config_data)
        config.save()
        self.languages[language_code] = config
