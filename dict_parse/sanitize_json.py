#!/usr/bin/env python3
"""Sanitize a JSON dictionary file of string->string entries.

Features:
- Normalize Unicode to NFC
- Trim and collapse excessive whitespace in keys
- Remove control characters from values (preserve \n and \t)
- Resolve duplicate keys by merging or renaming
- Write UTF-8 JSON with indent
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from collections import OrderedDict

CONTROL_RE = re.compile(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]")
WHITESPACE_RE = re.compile(r"[ \t]{2,}")


def sanitize_key(k: str) -> str:
    if not isinstance(k, str):
        k = str(k)
    k = unicodedata.normalize("NFC", k)
    k = k.replace("\r", "")
    k = k.strip()
    k = WHITESPACE_RE.sub(" ", k)
    return k


def sanitize_value(v: str) -> str:
    if v is None:
        return ""
    if not isinstance(v, str):
        v = str(v)
    v = unicodedata.normalize("NFC", v)
    # remove control chars except newline and tab
    v = CONTROL_RE.sub("", v)
    v = v.replace("\r\n", "\n").replace("\r", "\n")
    # collapse multiple spaces but keep paragraphs/newlines
    v = WHITESPACE_RE.sub(" ", v)
    v = v.strip()
    return v


def load_json_text(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sanitize_dict(d: dict, merge_duplicates: bool = True) -> OrderedDict:
    out = OrderedDict()
    dup_count = 0
    for raw_k, raw_v in d.items():
        k = sanitize_key(raw_k)
        v = sanitize_value(raw_v)
        if k in out:
            dup_count += 1
            if merge_duplicates:
                # merge preserving previous content
                prev = out[k]
                if prev and v:
                    out[k] = prev + "\n\n---\n\n" + v
                elif v:
                    out[k] = v
            else:
                # create unique key
                i = 1
                newk = f"{k}_dup{i}"
                while newk in out:
                    i += 1
                    newk = f"{k}_dup{i}"
                out[newk] = v
        else:
            out[k] = v
    return out


def write_json(obj: dict, path: str) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Sanitize JSON dictionary file")
    parser.add_argument("-i", "--input", required=True, help="Input JSON file")
    parser.add_argument("-o", "--output", required=False, help="Output JSON file (default: overwrite input with .sanitized.json)")
    parser.add_argument("--no-merge", dest="merge", action="store_false", help="Do not merge duplicate keys; instead rename duplicates")
    args = parser.parse_args(argv)

    inp = args.input
    if not os.path.exists(inp):
        print(f"Input file not found: {inp}", file=sys.stderr)
        sys.exit(2)

    out_path = args.output or os.path.splitext(inp)[0] + ".sanitized.json"

    try:
        data = load_json_text(inp)
    except Exception as e:
        print(f"Failed to parse JSON {inp}: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, dict):
        print("Expected top-level JSON object (dict mapping)", file=sys.stderr)
        sys.exit(2)

    sanitized = sanitize_dict(data, merge_duplicates=args.merge)
    write_json(sanitized, out_path)

    print(f"Sanitized {len(data)} entries -> {len(sanitized)} entries written to: {out_path}")


if __name__ == "__main__":
    main()
