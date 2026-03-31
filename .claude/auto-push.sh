#!/bin/bash
# Auto-push vers GitHub après chaque modification

REPO="/Users/marius0910/Documents/claude code/Techflair"

cd "$REPO" || exit 1

# Ajouter tous les fichiers modifiés
git add -A

# Vérifier s'il y a des changements à commiter
if git diff --cached --quiet; then
  exit 0  # Rien à commiter
fi

# Commiter
git commit -m "Auto-save: $(date '+%Y-%m-%d %H:%M')"

# Pull + push
git pull --rebase origin main 2>&1
git push origin main 2>&1
