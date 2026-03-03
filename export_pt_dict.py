import sqlite3
import json
import re

DB_PATH = 'palabras.db'
OUTPUT_PATH = 'dictionaries/portuguese.dict.json'

# POS labels that appear at the start of definition sections on dicio.com.br
POS_PATTERNS = [
    'adjetivo', 'advérbio', 'artigo definido', 'artigo indefinido',
    'conjunção', 'contração', 'expressão', 'interjeição',
    'numeral', 'prefixo', 'preposição', 'pronome', 'substantivo',
    'verbo',
]

def is_pos_line(line):
    """Check if a line is a part-of-speech header."""
    stripped = line.strip().lower()
    for pos in POS_PATTERNS:
        if stripped.startswith(pos):
            return True
    return False

def parse_definition(raw_text):
    """Parse a raw dicio.com.br definition into structured senses."""
    lines = [l.strip() for l in raw_text.split('\n') if l.strip()]

    senses = []
    current_pos = None
    current_defs = []

    for line in lines:
        if is_pos_line(line):
            # Save previous sense group if it has definitions
            if current_defs:
                senses.append({
                    "pos": current_pos or "",
                    "definitions": list(current_defs)
                })
                current_defs = []
            current_pos = line.strip()
        else:
            # Skip etymology lines at the end
            if line.lower().startswith('etimologia (origem'):
                break
            current_defs.append(line)

    # Don't forget the last group
    if current_defs:
        senses.append({
            "pos": current_pos or "",
            "definitions": list(current_defs)
        })

    return senses

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT palavra, definicion FROM palavras
        WHERE definicion != 'NOT_FOUND'
        ORDER BY palavra
    """)

    dictionary = []
    for palavra, definicion in cursor:
        senses = parse_definition(definicion)
        if senses:
            dictionary.append({
                "word": palavra,
                "senses": senses
            })

    conn.close()

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print(f"Exported {len(dictionary)} words to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
