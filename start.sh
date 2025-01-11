#!/bin/bash

# Aktiviere die Python-Umgebung
source venv/bin/activate

# Starte den Backend-Server
cd src
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
