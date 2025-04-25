#!/bin/bash
set -eo pipefail
source /opt/venv/bin/activate        # Codespace venv 경로
python scripts/scraper.py
