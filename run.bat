@echo off
cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer from https://www.python.org/downloads/
  echo Tick "Add Python to PATH" during setup, then run this file again.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\streamlit.exe" (
  echo First-time setup. This can take a few minutes...
  python -m venv .venv
  call .venv\Scripts\activate
  python -m pip install --upgrade pip
  pip install -r requirements.txt
) else (
  call .venv\Scripts\activate
)

streamlit run markitdown_app.py
pause
