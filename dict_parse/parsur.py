import re
import json

def parse_hindi_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # The file content as is, no need to strip line numbers 
        # because the ones I saw were added by the 'read' tool.
        content = f.read()

    # Split by double newlines to get entries
    # The file seems to use double newlines (or more) as entry separators
    raw_entries = re.split(r'\n\s*\n+', content)

    parsed_data = []

    for entry_text in raw_entries:
        entry_text = entry_text.strip().replace('\n', ' ')
        if not entry_text:
            continue
            
        # The word is at the beginning, usually followed by | or [ or ( or space
        # We split by these characters and take the first part
        word_match = re.match(r'^([^\|\[\(\s]+)', entry_text)
        if not word_match:
            continue
            
        word = word_match.group(1)
        remainder = entry_text[len(word):].strip()
        
        # Clean up the remainder start (remove leading | and spaces)
        remainder = re.sub(r'^[\| \.\)\]]+', '', remainder).strip()

        senses = []
        # Look for POS tags like [सं-पु.] or [सं-ख्री.|
        # We handle cases where the closing bracket might be replaced by a pipe
        parts = re.split(r'(\[[^\]\|]+[\]\|])', remainder)
        
        if len(parts) == 1:
            # No explicit POS tags, treat everything as one sense
            defs = clean_definitions(remainder)
            if defs:
                senses.append({
                    "pos": None,
                    "definitions": defs
                })
        else:
            # Before the first POS tag there might be some general definitions or metadata
            if parts[0].strip():
                defs = clean_definitions(parts[0])
                if defs:
                    senses.append({
                        "pos": None,
                        "definitions": defs
                    })
            
            for i in range(1, len(parts), 2):
                pos_tag = parts[i].strip('[]|').strip()
                def_blob = parts[i+1] if i+1 < len(parts) else ""
                defs = clean_definitions(def_blob)
                if defs:
                    senses.append({
                        "pos": pos_tag,
                        "definitions": defs
                    })

        if senses:
            parsed_data.append({
                "word": word,
                "senses": senses
            })

    return parsed_data

def clean_definitions(blob):
    # Remove leading separators and artifacts
    blob = re.sub(r'^[\|\.\s!:]+', '', blob)
    
    # Split by numbers or Hindi markers
    # Supports "1.", "२.", "।.", "। "
    raw_defs = re.split(r'(?:\d+|[०-९]+|।)\.?\s+', blob)
    
    cleaned = []
    for d in raw_defs:
        d = d.strip()
        # Remove trailing artifacts
        d = re.sub(r'[।\|\s]+$', '', d)
        # Filter out metadata like (सं.) or very short artifacts
        if d and len(d) > 1 and not re.match(r'^\([^)]+\)$', d):
            cleaned.append(d)
    
    # Fallback to semicolon split if no numbered definitions
    if len(cleaned) <= 1:
        text = cleaned[0] if cleaned else blob.strip()
        text = re.sub(r'[।\|\s]+$', '', text)
        if ';' in text:
            return [sd.strip() for sd in text.split(';') if sd.strip()]
        elif text and len(text) > 1 and not re.match(r'^\([^)]+\)$', text):
            return [text]
    
    return cleaned


if __name__ == "__main__":
    import os
    file_path = "/Users/enrique/Desktop/fun_repos/language-lilypad/raw_dictionaries/hindi.txt"
    output_path = "dictionaries/hindi.dict.json"

    if os.path.exists(file_path):
        results = parse_hindi_dictionary(file_path)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print(f"Total words parsed: {len(results)}")
        print(f"Saved to {output_path}")

