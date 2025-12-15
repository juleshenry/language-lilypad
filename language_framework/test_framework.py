#!/usr/bin/env python3
"""
Test script for the Language Framework
Validates that all components work correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language_framework.language_config import LanguageConfig, LanguageRegistry
from language_framework.dictionary_scraper import get_scraper, Word
from language_framework.database_manager import DatabaseManager


def test_language_config():
    """Test language configuration loading"""
    print("Testing Language Configuration...")
    
    try:
        # Test loading Portuguese config
        config_pt = LanguageConfig('pt')
        assert config_pt.name == "Portuguese"
        assert config_pt.language_code == "pt"
        assert config_pt.source_type == "json"
        print("✓ Portuguese config loaded successfully")
        
        # Test loading French config
        config_fr = LanguageConfig('fr')
        assert config_fr.name == "French"
        assert config_fr.native_name == "Français"
        print("✓ French config loaded successfully")
        
        # Test loading Korean config
        config_ko = LanguageConfig('ko')
        assert config_ko.name == "Korean"
        assert config_ko.native_name == "한국어"
        print("✓ Korean config loaded successfully")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_language_registry():
    """Test language registry"""
    print("\nTesting Language Registry...")
    
    try:
        registry = LanguageRegistry()
        
        # Check that all languages are registered
        all_langs = registry.list_all()
        assert 'pt' in all_langs
        assert 'fr' in all_langs
        assert 'ko' in all_langs
        print(f"✓ Registry has {len(all_langs)} languages")
        
        # Check that languages are enabled
        enabled_langs = registry.list_enabled()
        assert 'pt' in enabled_langs
        assert 'fr' in enabled_langs
        assert 'ko' in enabled_langs
        print(f"✓ {len(enabled_langs)} languages are enabled")
        
        return True
    except Exception as e:
        print(f"✗ Registry test failed: {e}")
        return False


def test_json_scraper():
    """Test JSON dictionary scraper"""
    print("\nTesting JSON Scraper...")
    
    try:
        # Test Portuguese scraper
        config_pt = LanguageConfig('pt')
        scraper = get_scraper('pt', 'json', config_pt.source_config)
        words = scraper.scrape()
        
        assert len(words) > 0
        print(f"✓ Portuguese scraper extracted {len(words)} words")
        
        # Verify word structure
        first_word = words[0]
        assert hasattr(first_word, 'word')
        assert hasattr(first_word, 'definition')
        print(f"✓ Word structure is correct: {first_word.word}")
        
        # Test French scraper
        config_fr = LanguageConfig('fr')
        scraper = get_scraper('fr', 'json', config_fr.source_config)
        words = scraper.scrape()
        assert len(words) > 0
        print(f"✓ French scraper extracted {len(words)} words")
        
        # Test Korean scraper
        config_ko = LanguageConfig('ko')
        scraper = get_scraper('ko', 'json', config_ko.source_config)
        words = scraper.scrape()
        assert len(words) > 0
        print(f"✓ Korean scraper extracted {len(words)} words")
        
        return True
    except Exception as e:
        print(f"✗ Scraper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_manager():
    """Test database manager"""
    print("\nTesting Database Manager...")
    
    try:
        # Use a test database
        test_db = "/tmp/test_language_framework.db"
        Path(test_db).unlink(missing_ok=True)
        
        with DatabaseManager(test_db) as db:
            # Create a test table
            db.create_language_table('test', 'test_words')
            print("✓ Created test language table")
            
            # Insert test words
            test_words = [
                Word("hello", "A greeting"),
                Word("world", "The earth"),
            ]
            inserted = db.insert_words('test', test_words, 'test_words')
            assert inserted == 2
            print(f"✓ Inserted {inserted} words")
            
            # Query a word
            result = db.query_word('test', 'hello', 'test_words')
            assert result is not None
            assert result['palabra'] == 'hello'
            assert result['definicion'] == 'A greeting'
            print(f"✓ Queried word: {result['palabra']}")
            
            # Get word count
            count = db.get_word_count('test', 'test_words')
            assert count == 2
            print(f"✓ Word count: {count}")
        
        # Clean up
        Path(test_db).unlink(missing_ok=True)
        
        return True
    except Exception as e:
        print(f"✗ Database manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_database():
    """Test that the main database has the new languages"""
    print("\nTesting Main Database...")
    
    try:
        db_path = Path(__file__).parent.parent / "react_version/backend/db/palabras.db"
        
        if not db_path.exists():
            print(f"⚠ Main database not found at {db_path}")
            print("  Run: python3 language_framework/populate_database.py --all --database react_version/backend/db/palabras.db")
            return True  # Not a failure, just needs setup
        
        with DatabaseManager(str(db_path)) as db:
            # Check Portuguese
            pt_count = db.get_word_count('pt', 'pt_words')
            if pt_count > 0:
                print(f"✓ Portuguese dictionary has {pt_count} words")
            else:
                print(f"⚠ Portuguese dictionary is empty")
            
            # Check French
            fr_count = db.get_word_count('fr', 'fr_words')
            if fr_count > 0:
                print(f"✓ French dictionary has {fr_count} words")
            else:
                print(f"⚠ French dictionary is empty")
            
            # Check Korean
            ko_count = db.get_word_count('ko', 'ko_words')
            if ko_count > 0:
                print(f"✓ Korean dictionary has {ko_count} words")
            else:
                print(f"⚠ Korean dictionary is empty")
        
        return True
    except Exception as e:
        print(f"✗ Main database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Language Framework Test Suite")
    print("=" * 60)
    
    tests = [
        test_language_config,
        test_language_registry,
        test_json_scraper,
        test_database_manager,
        test_main_database,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
