#!/usr/bin/env bash
# Simple runner for macOS/Linux in the project root
set -e
python3 -m venv .venv
source .venv/bin/activate
echo "Installing dependencies... (this may take a few minutes)"
pip install --upgrade pip
pip install -r requirements.txt
echo "Starting server..."
python -m uvicorn backend.app.app:app --reload