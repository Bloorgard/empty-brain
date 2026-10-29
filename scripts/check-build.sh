#!/usr/bin/env bash
set -euo pipefail
output="${1:-public}"
node scripts/check-links.mjs
node quartz/bootstrap-cli.mjs build --output "$output"
python3 scripts/check-site-links.py "$output"
echo "BUILD OK"
