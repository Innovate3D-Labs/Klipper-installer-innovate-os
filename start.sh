#!/bin/bash

# Prüfe ob das Script als root läuft
if [ "$EUID" -ne 0 ]; then 
    echo "Bitte als root ausführen: sudo bash start.sh"
    exit 1
fi

# Setze Umgebungsvariablen
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_PATH="$SCRIPT_DIR/venv"
PYTHON="$VENV_PATH/bin/python3"
PIP="$VENV_PATH/bin/pip"

# Erstelle virtuelle Umgebung wenn sie nicht existiert
if [ ! -d "$VENV_PATH" ]; then
    echo "Erstelle virtuelle Python-Umgebung..."
    python3 -m venv "$VENV_PATH"
fi

# Aktiviere virtuelle Umgebung und installiere Abhängigkeiten
echo "Installiere/Aktualisiere Python-Abhängigkeiten..."
source "$VENV_PATH/bin/activate"
$PIP install -r "$SCRIPT_DIR/requirements.txt"

# Installiere und baue Frontend
echo "Installiere und baue Frontend..."
cd "$SCRIPT_DIR/src/frontend"
if [ ! -d "node_modules" ]; then
    echo "Installiere npm Pakete..."
    npm install
fi
echo "Baue Frontend..."
npm run build

# Debugging-Ausgabe
echo "Debugging: Prüfe Frontend-Build..."
ls -la "$SCRIPT_DIR/src/frontend/dist"

# Starte den Server mit Debug-Ausgabe
echo "Starte Klipper Installer Server..."
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
$PYTHON -m uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
