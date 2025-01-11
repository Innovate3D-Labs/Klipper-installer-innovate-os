#!/bin/bash

# Aktiviere die Python-Umgebung
source venv/bin/activate

# Wechsle in das src Verzeichnis
cd src

# Starte den Server
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload --app-dir .
