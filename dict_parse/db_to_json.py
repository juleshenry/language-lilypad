#!/usr/bin/env python3
"""
Convert SQLite database to indexed JSON files.

This script reads a SQLite database containing dictionary words and definitions,
and splits the data into multiple JSON files, each less than 25MB in size.
Each JSON file is named as first_word__last_word.json for easy lookup.
"""

import sqlite3
import json
import os
import sys
from pathlib import Path


def get_database_size_mb(db_path):
    """Get the size of the database file in MB."""
    return os.path.getsize(db_path) / (1024 * 1024)


def fetch_all_words(db_path):
    """Fetch all words and definitions from the database, sorted alphabetically."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Fetch all words sorted alphabetically
        cursor.execute("SELECT palabra, definicion FROM palabras ORDER BY palabra")
        words = cursor.fetchall()
        
        return words
    except sqlite3.DatabaseError as e:
        print(f"Error reading database: {e}")
        print("Please ensure the database file is valid and not corrupted.")
        sys.exit(1)
    except sqlite3.OperationalError as e:
        print(f"Database operation error: {e}")
        print("Please ensure the database has a 'palabras' table with 'palabra' and 'definicion' columns.")
        sys.exit(1)
    finally:
        if conn is not None:
            conn.close()


def estimate_entry_size(palabra, definicion):
    """
    Estimate the size of a single JSON entry in bytes.
    
    Format in JSON: "  \"palabra\": \"definicion\",\n"
    Includes indent (2 spaces), quotes, colon, comma, and newline.
    """
    return 2 + 1 + len(palabra.encode('utf-8')) + 1 + 2 + 1 + len(definicion.encode('utf-8')) + 1 + 2


def split_into_chunks(words, max_size_bytes=25 * 1024 * 1024):
    """
    Split words into chunks, each less than max_size_bytes.
    
    Args:
        words: List of (palabra, definicion) tuples
        max_size_bytes: Maximum size in bytes for each chunk (default: 25MB)
    
    Returns:
        List of chunks, where each chunk is a list of (palabra, definicion) tuples
    """
    chunks = []
    current_chunk = []
    estimated_size = 0
    
    # Use a threshold slightly below max to account for minor estimation errors
    # This ensures we never exceed the limit even with estimation inaccuracies
    safe_threshold = max_size_bytes * 0.95  # 95% of max size
    
    for palabra, definicion in words:
        # Estimate size of this single entry using helper function
        entry_size = estimate_entry_size(palabra, definicion)
        
        # Check if adding this entry would exceed threshold
        if estimated_size + entry_size > safe_threshold and current_chunk:
            # Save current chunk and start new one
            chunks.append(current_chunk)
            current_chunk = []
            estimated_size = 4  # JSON object overhead: "{\n}\n"
        
        current_chunk.append((palabra, definicion))
        estimated_size += entry_size
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def sanitize_word_for_filename(word):
    """
    Sanitize a word to be safely used as part of a filename.
    
    Removes or replaces characters that are problematic in filenames across different OS.
    """
    # Replace characters that might cause issues in filenames
    word = word.replace('/', '_')
    word = word.replace('\\', '_')
    word = word.replace('|', '_')
    word = word.replace(':', '_')
    word = word.replace('*', '_')
    word = word.replace('?', '_')
    word = word.replace('"', '_')
    word = word.replace('<', '_')
    word = word.replace('>', '_')
    word = word.replace('\0', '_')  # Null byte
    word = word.replace('\n', '_')  # Newline
    word = word.replace('\t', '_')  # Tab
    word = word.strip()
    
    # Handle empty strings after sanitization
    if not word:
        return "empty"
    
    # Limit length to avoid filesystem limits (leave room for __, .json and other word)
    max_word_length = 100
    if len(word) > max_word_length:
        word = word[:max_word_length]
    
    return word


def write_json_files(chunks, output_dir):
    """
    Write chunks to JSON files with naming format first_word__last_word.json.
    
    Args:
        chunks: List of chunks to write
        output_dir: Directory to write JSON files to
    
    Returns:
        List of (filename, size_in_mb, word_count) tuples
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    file_info = []
    
    for chunk in chunks:
        first_word = sanitize_word_for_filename(chunk[0][0])
        last_word = sanitize_word_for_filename(chunk[-1][0])
        
        # Create filename
        filename = f"{first_word}__{last_word}.json"
        filepath = output_path / filename
        
        # Convert chunk to dictionary
        data = {palabra: definicion for palabra, definicion in chunk}
        
        # Write JSON file with error handling
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error writing file {filename}: {e}")
            print("Please check disk space and write permissions.")
            sys.exit(1)
        
        # Get file size
        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
        word_count = len(chunk)
        
        file_info.append((filename, file_size_mb, word_count))
        
        print(f"Created: {filename} ({file_size_mb:.2f} MB, {word_count} words)")
    
    return file_info


def main():
    """Main function to convert database to JSON files."""
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python db_to_json.py <database_path> [output_directory]")
        print("Example: python db_to_json.py ../palabras.db ./json_output")
        sys.exit(1)
    
    db_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./json_output"
    
    # Validate database file
    if not os.path.exists(db_path):
        print(f"Error: Database file not found: {db_path}")
        print("Please check the file path and ensure the database file exists.")
        print(f"Example: python3 {sys.argv[0]} /path/to/palabras.db ./json_output")
        sys.exit(1)
    
    # Check if it's a file (not a directory)
    if not os.path.isfile(db_path):
        print(f"Error: Path exists but is not a file: {db_path}")
        sys.exit(1)
    
    print(f"Converting database: {db_path}")
    print(f"Output directory: {output_dir}")
    print(f"Database size: {get_database_size_mb(db_path):.2f} MB")
    print()
    
    # Fetch all words
    print("Fetching words from database...")
    words = fetch_all_words(db_path)
    print(f"Total words: {len(words)}")
    print()
    
    # Split into chunks
    print("Splitting into chunks (max 25MB each)...")
    chunks = split_into_chunks(words)
    print(f"Created {len(chunks)} chunks")
    print()
    
    # Write JSON files
    print("Writing JSON files...")
    file_info = write_json_files(chunks, output_dir)
    print()
    
    # Print summary
    print("Summary:")
    print(f"  Total files created: {len(file_info)}")
    print(f"  Total words: {len(words)}")
    
    if file_info:
        total_size = sum(size for _, size, _ in file_info)
        print(f"  Total size: {total_size:.2f} MB")
        print(f"  Average file size: {total_size / len(file_info):.2f} MB")
    else:
        print("  No files created (database may be empty)")
        return
    
    # Verify all files are under 25MB
    oversized = [f for f, size, _ in file_info if size >= 25]
    if oversized:
        print()
        print(f"WARNING: {len(oversized)} files are 25MB or larger:")
        for filename in oversized:
            print(f"  - {filename}")
    else:
        print("  ✓ All files are under 25MB")
    
    print()
    print("Conversion complete!")


if __name__ == "__main__":
    main()
