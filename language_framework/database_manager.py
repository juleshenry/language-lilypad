"""
Database Manager for Multi-Language Dictionaries
Handles database operations for storing and querying dictionaries in multiple languages
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Dict
from .dictionary_scraper import Word


class DatabaseManager:
    """Manages multi-language dictionary databases"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize database manager
        
        Args:
            db_path: Path to the SQLite database file
        """
        if db_path is None:
            # Default to the main palabras.db in the repo root
            db_path = Path(__file__).parent.parent / "palabras.db"
        
        self.db_path = Path(db_path)
        self.conn = None
        self._ensure_connection()
    
    def _ensure_connection(self):
        """Ensure database connection is established"""
        if self.conn is None:
            self.conn = sqlite3.connect(str(self.db_path))
    
    def create_language_table(self, language_code: str, table_name: str = None) -> None:
        """
        Create a table for a specific language
        
        Args:
            language_code: ISO language code
            table_name: Custom table name (defaults to language_code_words)
        """
        if table_name is None:
            table_name = f"{language_code}_words"
        
        self._ensure_connection()
        cursor = self.conn.cursor()
        
        # Create the words table for this language
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                palabra TEXT PRIMARY KEY,
                definicion TEXT,
                metadata TEXT
            )
        """)
        
        # Create an index for faster lookups
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{table_name}_palabra 
            ON {table_name}(palabra)
        """)
        
        self.conn.commit()
    
    def insert_words(self, language_code: str, words: List[Word], 
                    table_name: str = None, batch_size: int = 1000) -> int:
        """
        Insert words into the database
        
        Args:
            language_code: ISO language code
            words: List of Word objects to insert
            table_name: Custom table name
            batch_size: Number of words to insert per batch
            
        Returns:
            Number of words successfully inserted
        """
        if table_name is None:
            table_name = f"{language_code}_words"
        
        self._ensure_connection()
        cursor = self.conn.cursor()
        
        inserted_count = 0
        batch = []
        
        for word in words:
            # Convert metadata to JSON string if present
            metadata_json = str(word.metadata) if word.metadata else None
            
            batch.append((word.word, word.definition, metadata_json))
            
            if len(batch) >= batch_size:
                inserted_count += self._insert_batch(cursor, table_name, batch)
                batch = []
        
        # Insert remaining words
        if batch:
            inserted_count += self._insert_batch(cursor, table_name, batch)
        
        self.conn.commit()
        return inserted_count
    
    def _insert_batch(self, cursor, table_name: str, batch: List[tuple]) -> int:
        """Insert a batch of words"""
        inserted = 0
        for word_data in batch:
            try:
                cursor.execute(f"""
                    INSERT INTO {table_name} (palabra, definicion, metadata)
                    VALUES (?, ?, ?)
                """, word_data)
                inserted += 1
            except sqlite3.IntegrityError:
                # Word already exists, skip
                pass
        return inserted
    
    def query_word(self, language_code: str, word: str, 
                   table_name: str = None) -> Optional[Dict]:
        """
        Query a word definition
        
        Args:
            language_code: ISO language code
            word: Word to look up
            table_name: Custom table name
            
        Returns:
            Dictionary with word, definition, and metadata, or None if not found
        """
        if table_name is None:
            table_name = f"{language_code}_words"
        
        self._ensure_connection()
        cursor = self.conn.cursor()
        
        try:
            cursor.execute(f"""
                SELECT palabra, definicion, metadata
                FROM {table_name}
                WHERE palabra = ?
            """, (word,))
            
            result = cursor.fetchone()
            if result:
                return {
                    "palabra": result[0],
                    "definicion": result[1],
                    "metadata": result[2]
                }
        except sqlite3.OperationalError:
            # Table doesn't exist
            return None
        
        return None
    
    def get_word_count(self, language_code: str, table_name: str = None) -> int:
        """
        Get the count of words in a language table
        
        Args:
            language_code: ISO language code
            table_name: Custom table name
            
        Returns:
            Number of words in the table
        """
        if table_name is None:
            table_name = f"{language_code}_words"
        
        self._ensure_connection()
        cursor = self.conn.cursor()
        
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return cursor.fetchone()[0]
        except sqlite3.OperationalError:
            # Table doesn't exist
            return 0
    
    def list_tables(self) -> List[str]:
        """
        List all tables in the database
        
        Returns:
            List of table names
        """
        self._ensure_connection()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        
        return [row[0] for row in cursor.fetchall()]
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
