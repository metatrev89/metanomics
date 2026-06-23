#!/bin/bash
# Publish to metanomics.org — commits, pushes, and pings all search engines.
#
# Usage:
#   ./publish.sh "Your commit message"
#
# Example:
#   ./publish.sh "Add new post: Economy of Zion overview"

set -e
cd "$(dirname "$0")"

MSG="${1:-Update site content}"

echo ""
echo "================================================"
echo "  Metanomics Publisher"
echo "================================================"

echo ""
echo "[1/2] Pushing to GitHub..."
echo "------------------------------------------------"
git add -A
git commit -m "$MSG" || echo "Nothing new to commit."
git pull origin main --rebase
git push origin main

echo ""
echo "[2/2] Pinging search engines..."
echo "------------------------------------------------"
python3 scripts/ping_all.py

echo ""
echo "================================================"
echo "  Published! metanomics.org is live & indexed."
echo "================================================"
echo ""
