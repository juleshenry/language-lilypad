import requests
from bs4 import BeautifulSoup
import sqlite3
import time
import os
import csv
import unicodedata
from tqdm import tqdm

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def log_failure(word, log_path='failed_scrapes.log'):
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"{word}\n")

def create_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS palavras (
            palavra TEXT PRIMARY KEY,
            definicion TEXT
        )
    ''')
    conn.commit()
    return conn

def scrape_word(word):
    # Try the original word first, then the unaccented version
    slugs = [word, strip_accents(word)]
    # Remove duplicates if the word had no accents
    slugs = list(dict.fromkeys(slugs))
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for slug in slugs:
        url = f"https://www.dicio.com.br/{slug}/"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                significado = soup.find('p', class_='significado')
                if significado:
                    return significado.get_text(separator="\n").strip()
            elif response.status_code == 404:
                continue # Try next slug
        except Exception as e:
            return None # Treat as temp failure
    
    return "NOT_FOUND"

def main():
    csv_path = 'unitex-pt-br/data/mirror/DELAS.csv'
    db_path = 'palabras.db'
    log_path = 'failed_scrapes.log'
    
    if os.path.exists(log_path):
        os.remove(log_path)
        print(f"Cleared {log_path}")

    if not os.path.exists(csv_path):
        print(f"{csv_path} not found.")
        return

    conn = create_db(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM palavras WHERE definicion != 'NOT_FOUND'")
    found_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM palavras WHERE definicion = 'NOT_FOUND'")
    not_found_count = cursor.fetchone()[0]
    print(f"Resuming: {found_count} definitions found, {not_found_count} not found (skipping both).")

    print("Loading words from CSV...")
    words_set = set()
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row['canonical_form'].strip().lower()
            if word:
                words_set.add(word)
    
    sorted_words = sorted(list(words_set))
    total_words = len(sorted_words)
    print(f"Total unique words to process: {total_words}")

    print("Starting continuous scrape with ETA tracking...")
    
    try:
        with tqdm(total=total_words, desc="Scraping Dicio", unit="word") as pbar:
            for word in sorted_words:
                # Check if already in DB
                cursor.execute("SELECT 1 FROM palavras WHERE palavra = ?", (word,))
                if cursor.fetchone():
                    pbar.update(1)
                    continue

                definition = scrape_word(word)
                
                if definition == "NOT_FOUND":
                    log_failure(word, log_path)
                    cursor.execute("INSERT OR REPLACE INTO palavras (palavra, definicion) VALUES (?, ?)", (word, definition))
                    conn.commit()
                    # pbar.write(f"[-] '{word}' not found.")
                elif definition:
                    cursor.execute("INSERT OR REPLACE INTO palavras (palavra, definicion) VALUES (?, ?)", (word, definition))
                    conn.commit()
                    # pbar.write(f"[+] Scraped '{word}'.")
                else:
                    pbar.write(f"[!] Rate limit or network error for '{word}'. Sleeping...")
                    time.sleep(10)
                
                pbar.update(1)
                time.sleep(1.2)
            
    except KeyboardInterrupt:
        print("\nScraping interrupted. Progress saved.")
    finally:
        conn.close()
        print("Done.")

if __name__ == "__main__":
    main()
