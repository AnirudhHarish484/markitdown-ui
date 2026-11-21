#!/usr/bin/env bash
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 not found. Install Python 3.10 or newer from https://www.python.org/downloads/"
  exit 1
fi

if [ ! -x ".venv/bin/streamlit" ]; then
  echo "First-time setup. This can take a few minutes..."
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi

streamlit run markitdown_app.py
