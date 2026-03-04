#!/bin/bash

# Get list of issues with "Add ... language support"
issues=$(gh issue list --limit 100 --state open --json title --jq '.[] | .title' | grep "Add .* language support")

echo "Comparing Issues to Branches..."
echo "--------------------------------"

while IFS= read -r title; do
    # Extract language name and sanitize for branch
    # e.g., "Add Central Aymara language support" -> "aymara"
    # e.g., "Add Standard Arabic language support" -> "standard-arabic"
    
    lang=$(echo "$title" | sed -E 's/Add (.*) language support/\1/' | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/(//g' | sed 's/)//g')
    
    # Handle specific manual branch naming overrides if any (e.g. sorani-kurdish)
    if [[ "$lang" == *"central-kurdish-sorani"* ]]; then lang="sorani-kurdish"; fi
    if [[ "$lang" == *"dinkas-south-sudan"* ]]; then lang="dinka"; fi
    if [[ "$lang" == *"taizzi-adeni-arabic"* ]]; then lang="taizzi-adenic-arabic"; fi

    branch="feature/$lang"
    
    # Check if branch exists locally or remotely
    if git rev-parse --verify "$branch" >/dev/null 2>&1 || git rev-parse --verify "origin/$branch" >/dev/null 2>&1; then
        echo "✅ [FOUND]     Branch: $branch (Issue: $title)"
    else
        echo "❌ [MISSING]   Branch: $branch (Issue: $title)"
    fi
done <<< "$issues"
