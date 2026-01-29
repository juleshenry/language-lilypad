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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch all words sorted alphabetically
    cursor.execute("SELECT palabra, definicion FROM palabras ORDER BY palabra")
    words = cursor.fetchall()
    
    conn.close()
    return words


def estimate_json_size(data):
    """Estimate the size of JSON data in bytes."""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return len(json_str.encode('utf-8'))


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
    current_size = 2  # Start with 2 bytes for the empty object "{}"
    
    for palabra, definicion in words:
        # Estimate the size of this entry when added to JSON
        entry = {palabra: definicion}
        entry_size = estimate_json_size(entry)
        
        # Add some overhead for JSON formatting (commas, newlines, etc.)
        entry_size += 10
        
        # Check if adding this entry would exceed the limit
        if current_size + entry_size > max_size_bytes and current_chunk:
            # Save current chunk and start a new one
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 2
        
        current_chunk.append((palabra, definicion))
        current_size += entry_size
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def sanitize_filename(word):
    """Sanitize a word to be used in a filename."""
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
    return word.strip()


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
    
    for i, chunk in enumerate(chunks):
        first_word = sanitize_filename(chunk[0][0])
        last_word = sanitize_filename(chunk[-1][0])
        
        # Create filename
        filename = f"{first_word}__{last_word}.json"
        filepath = output_path / filename
        
        # Convert chunk to dictionary
        data = {palabra: definicion for palabra, definicion in chunk}
        
        # Write JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
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
    total_size = sum(size for _, size, _ in file_info)
    print(f"  Total size: {total_size:.2f} MB")
    print(f"  Average file size: {total_size / len(file_info):.2f} MB")
    
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
