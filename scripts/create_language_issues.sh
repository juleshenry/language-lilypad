#!/usr/bin/env bash
#
# create_language_issues.sh
#
# Reads nllb.txt and creates a GitHub issue for each language to be added
# to language-lilypad. Skips the header line and languages that already
# have dictionary support (Spanish, Portuguese, Hindi).
#
# Prerequisites:
#   - gh CLI installed and authenticated
#   - Run from the repo root (or set REPO below)
#
# Usage:
#   ./create_language_issues.sh
#   ./create_language_issues.sh --start-from 3   # resume from the 3rd language entry

set -euo pipefail

NLLB_FILE="nllb.txt"
REPO="juleshenry/language-lilypad"
START_FROM=1

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --start-from)
      START_FROM="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--start-from N]"
      exit 1
      ;;
  esac
done

# Languages that already have dictionary data — skip these
SKIP_CODES=("spa" "por" "hin")

if [[ ! -f "$NLLB_FILE" ]]; then
  echo "Error: $NLLB_FILE not found. Run this script from the repo root."
  exit 1
fi

if ! command -v gh &> /dev/null; then
  echo "Error: GitHub CLI (gh) is not installed. Install it from https://cli.github.com/"
  exit 1
fi

# Verify authentication
if ! gh auth status &> /dev/null; then
  echo "Error: Not authenticated with GitHub CLI. Run 'gh auth login' first."
  exit 1
fi

created=0
skipped=0
failed=0
line_num=0

# Read the CSV, skip the header line
tail -n +2 "$NLLB_FILE" | while IFS=',' read -r code language script; do
  line_num=$((line_num + 1))

  # Trim leading/trailing whitespace (bash-native, safe for quotes/apostrophes)
  code="${code#"${code%%[![:space:]]*}"}"
  code="${code%"${code##*[![:space:]]}"}"
  language="${language#"${language%%[![:space:]]*}"}"
  language="${language%"${language##*[![:space:]]}"}"
  script="${script#"${script%%[![:space:]]*}"}"
  script="${script%"${script##*[![:space:]]}"}"

  # Skip languages that already have dictionary support
  skip=false
  for skip_code in "${SKIP_CODES[@]}"; do
    if [[ "$code" == "$skip_code" ]]; then
      skip=true
      break
    fi
  done

  if $skip; then
    echo "SKIP: $language ($code) — already supported"
    skipped=$((skipped + 1))
    continue
  fi

  # Skip entries before --start-from
  if [[ $line_num -lt $START_FROM ]]; then
    echo "SKIP: $language ($code) — before start-from ($START_FROM)"
    continue
  fi

  title="Add $language language support"
  body="## Add $language Language Support

**NLLB Code:** \`$code\`
**Script(s):** $script

### Tasks

- [ ] Source or scrape a $language dictionary (word → definition mappings)
- [ ] Parse dictionary data into the project's JSON format (see \`dictionaries/\` for examples)
- [ ] Generate chunked dictionary files (\`$code.dict.*.json\`)
- [ ] Add $language to the seed/import pipeline
- [ ] Add $language (\`$code\`) to \`languageOptions.js\` for the translation dropdown (if not already present)
- [ ] Verify translation works via the NLLB translation backend
- [ ] Test end-to-end: translate → define → hyperlinked definitions

### Context

This language is part of the [NLLB (No Language Left Behind)](https://ai.meta.com/research/no-language-left-behind/) model's supported languages. The NLLB code \`$code\` should be used for translation API calls.
"

  echo "Creating issue: $title ..."
  if gh issue create --repo "$REPO" --title "$title" --body "$body" --label "enhancement"; then
    created=$((created + 1))
  else
    echo "FAILED: Could not create issue for $language ($code)"
    failed=$((failed + 1))
  fi

  # Small delay to avoid hitting GitHub API rate limits
  sleep 1
done

echo ""
echo "Done!"
echo "  Created: $created"
echo "  Skipped: $skipped"
echo "  Failed:  $failed"
