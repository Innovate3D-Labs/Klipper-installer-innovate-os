#!/bin/bash

# Aktiviere die Python-Umgebung
source venv/bin/activate

# Setze den Python-Path und starte den Server
export PYTHONPATH="$PWD/src"
python3 -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000 --reload
