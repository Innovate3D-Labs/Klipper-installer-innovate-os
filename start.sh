#!/bin/bash

# Aktiviere die Python-Umgebung
source venv/bin/activate

# Installiere npm Abhängigkeiten und baue das Frontend
echo "Baue das Frontend..."
npm install
npm run build

# Starte den Backend-Server
echo "Starte den Backend-Server..."
cd src
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
