#!/usr/bin/env python3
"""
Database Population Tool
CLI tool to scrape and populate dictionaries for multiple languages
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path to import framework modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from language_framework.language_config import LanguageConfig, LanguageRegistry
from language_framework.dictionary_scraper import get_scraper
from language_framework.database_manager import DatabaseManager


def populate_language(language_code: str, db_path: str = None, verbose: bool = True):
    """
    Populate database with dictionary data for a specific language
    
    Args:
        language_code: ISO language code (e.g., 'pt', 'fr', 'ko', 'es')
        db_path: Path to database file (optional)
        verbose: Print verbose output
    """
    try:
        # Load language configuration
        config = LanguageConfig(language_code)
        
        if verbose:
            print(f"Loading {config.name} ({config.native_name}) dictionary...")
            print(f"Source type: {config.source_type}")
        
        # Get the appropriate scraper
        scraper = get_scraper(
            language_code=language_code,
            source_type=config.source_type,
            config=config.source_config
        )
        
        # Scrape the dictionary
        if verbose:
            print(f"Scraping dictionary data...")
        
        words = scraper.scrape()
        
        if verbose:
            print(f"Scraped {len(words)} words")
        
        if not words:
            print(f"Warning: No words found for {language_code}")
            return 0
        
        # Create database and insert words
        with DatabaseManager(db_path) as db:
            # Create table for this language
            table_name = config.database_table
            if verbose:
                print(f"Creating table: {table_name}")
            
            db.create_language_table(language_code, table_name)
            
            # Insert words
            if verbose:
                print(f"Inserting words into database...")
            
            inserted = db.insert_words(language_code, words, table_name)
            
            if verbose:
                print(f"Successfully inserted {inserted} words")
                total = db.get_word_count(language_code, table_name)
                print(f"Total words in {config.name} dictionary: {total}")
        
        return inserted
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"Make sure the dictionary file exists for language '{language_code}'")
        return 0
    except Exception as e:
        print(f"Error populating {language_code}: {e}")
        import traceback
        traceback.print_exc()
        return 0


def list_languages(verbose: bool = True):
    """List all available languages"""
    registry = LanguageRegistry()
    
    print("\nAvailable Languages:")
    print("-" * 60)
    
    for code in sorted(registry.list_all()):
        config = registry.get(code)
        status = "✓" if config.enabled else "✗"
        print(f"{status} {code:4s} | {config.name:15s} | {config.native_name}")
    
    print("-" * 60)
    print(f"\nTotal: {len(registry.list_all())} languages")
    print(f"Enabled: {len(registry.list_enabled())} languages")


def show_stats(db_path: str = None):
    """Show database statistics"""
    with DatabaseManager(db_path) as db:
        tables = db.list_tables()
        
        print("\nDatabase Statistics:")
        print("-" * 60)
        
        registry = LanguageRegistry()
        
        for table in sorted(tables):
            # Try to find language config for this table
            lang_name = table
            for code in registry.list_all():
                config = registry.get(code)
                if config.database_table == table:
                    lang_name = f"{config.name} ({code})"
                    break
            
            count = db.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{lang_name:30s} | {count:6d} words")
        
        print("-" * 60)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Populate language dictionaries in the database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Populate Portuguese dictionary
  python populate_database.py --language pt
  
  # Populate all enabled languages
  python populate_database.py --all
  
  # List available languages
  python populate_database.py --list
  
  # Show database statistics
  python populate_database.py --stats
        """
    )
    
    parser.add_argument(
        '-l', '--language',
        type=str,
        help='Language code to populate (e.g., pt, fr, ko, es)'
    )
    
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='Populate all enabled languages'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available languages'
    )
    
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show database statistics'
    )
    
    parser.add_argument(
        '-d', '--database',
        type=str,
        default=None,
        help='Path to database file (default: palabras.db in repo root)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode (less verbose output)'
    )
    
    args = parser.parse_args()
    
    verbose = not args.quiet
    
    # Handle list command
    if args.list:
        list_languages(verbose)
        return
    
    # Handle stats command
    if args.stats:
        show_stats(args.database)
        return
    
    # Handle populate commands
    if args.all:
        registry = LanguageRegistry()
        enabled_languages = registry.list_enabled()
        
        print(f"\nPopulating {len(enabled_languages)} languages...")
        print("=" * 60)
        
        total_words = 0
        for lang_code in enabled_languages:
            print(f"\n[{lang_code.upper()}]")
            inserted = populate_language(lang_code, args.database, verbose)
            total_words += inserted
        
        print("\n" + "=" * 60)
        print(f"Total words inserted: {total_words}")
        
    elif args.language:
        inserted = populate_language(args.language, args.database, verbose)
        if inserted == 0:
            sys.exit(1)
    else:
        parser.print_help()
        print("\nError: Please specify --language, --all, --list, or --stats")
        sys.exit(1)


if __name__ == "__main__":
    main()
