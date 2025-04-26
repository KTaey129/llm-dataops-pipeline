#!/bin/bash
set -eo pipefail
source /opt/venv/bin/activate
python scripts/preprocess.py
