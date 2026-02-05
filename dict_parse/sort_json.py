#!/usr/bin/env python3
"""Sort a JSON dictionary file by keys (lemmas) and write alphabetized output."""
import argparse
import json
import os
import sys
import unicodedata


def normalize_key(k: str) -> str:
    return unicodedata.normalize("NFC", k).casefold()


def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(obj, path: str):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def sort_file(inp: str, out: str):
    j = load_json(inp)
    if not isinstance(j, dict):
        print("Expected top-level JSON object mapping", file=sys.stderr)
        sys.exit(2)
    items = list(j.items())
    items.sort(key=lambda kv: normalize_key(kv[0]))
    ordered = {k: v for k, v in items}
    write_json(ordered, out)
    print(f"Wrote {len(ordered)} entries to {out}")


def main(argv=None):
    p = argparse.ArgumentParser(description="Sort JSON dictionary by key")
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=False)
    args = p.parse_args(argv)
    inp = args.input
    if not os.path.exists(inp):
        print(f"Input not found: {inp}", file=sys.stderr)
        sys.exit(2)
    out = args.output or os.path.splitext(inp)[0] + ".alpha.json"
    sort_file(inp, out)


if __name__ == "__main__":
    main()
