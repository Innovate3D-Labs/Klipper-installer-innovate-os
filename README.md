# Klipper Installer Innovate OS

Eine benutzerfreundliche Webanwendung zur Installation und Verwaltung von Klipper auf 3D-Druckern.

## Features

- Automatische Installation von Klipper und allen Abhängigkeiten
- Unterstützung verschiedener Druckermodelle mit vorkonfigurierten Einstellungen
- Einfacher Wechsel zwischen Fluidd und Mainsail Weboberflächen
- Echtzeit-Fortschrittsanzeige und Logging
- Benutzerfreundliche Weboberfläche

## Installation

```bash
# Clone das Repository
git clone https://github.com/Innovate3D-Labs/Klipper-installer-innovate-os.git
cd Klipper-installer-innovate-os

# Installiere die Abhängigkeiten
pip install -r requirements.txt

# Starte die Anwendung
python src/main.py
```

## Projektstruktur

```
.
├── config/                     # Druckerkonfigurationen
│   ├── ender3/
│   ├── voron_trident/
│   └── ratrig_vcore3/
├── src/
│   ├── backend/               # Python Backend (FastAPI)
│   │   ├── api/
│   │   ├── core/
│   │   └── services/
│   └── frontend/              # Vue.js Frontend
├── tests/                     # Unit und Integration Tests
└── docs/                      # Dokumentation
```

## Entwicklung

- Backend: FastAPI (Python)
- Frontend: Vue.js
- Datenbank: SQLite für lokale Konfigurationsspeicherung

## Lizenz

MIT
