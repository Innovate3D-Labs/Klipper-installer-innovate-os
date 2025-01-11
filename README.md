# Klipper Installer Innovate OS

Eine benutzerfreundliche Webanwendung zur Installation und Verwaltung von Klipper auf 3D-Druckern.

## Features

- Automatische Installation von Klipper und allen Abhängigkeiten
- Unterstützung verschiedener Druckermodelle mit vorkonfigurierten Einstellungen
- Einfacher Wechsel zwischen Fluidd und Mainsail Weboberflächen
- Echtzeit-Fortschrittsanzeige und Logging
- Benutzerfreundliche Weboberfläche

## Entwicklung

### Voraussetzungen

- Node.js >= 18
- Python >= 3.11
- Docker (optional)

### Installation für Entwicklung

```bash
# Clone das Repository
git clone https://github.com/Innovate3D-Labs/Klipper-installer-innovate-os.git
cd Klipper-installer-innovate-os

# Frontend-Abhängigkeiten installieren
npm install

# Backend-Abhängigkeiten installieren
pip install -r requirements.txt

# Frontend-Entwicklungsserver starten
npm run dev

# Backend-Entwicklungsserver starten
uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker-Deployment

```bash
# Build und Start mit Docker Compose
docker-compose up --build
```

Die Anwendung ist dann unter http://localhost verfügbar.

## Projektstruktur

```
.
├── config/                     # Druckerkonfigurationen
│   ├── ender3/
│   ├── voron_trident/
│   └── ratrig_vcore3/
├── src/
│   ├── backend/               # Python Backend (FastAPI)
│   │   ├── api/              # API-Routen
│   │   ├── core/             # Kernfunktionen
│   │   └── services/         # Dienste
│   └── frontend/             # Vue.js Frontend
│       ├── components/       # Vue-Komponenten
│       ├── views/           # Seitenansichten
│       └── js/              # JavaScript-Module
├── tests/                    # Unit und Integration Tests
└── docs/                    # Dokumentation

## Entwicklung

- Backend: FastAPI (Python)
- Frontend: Vue.js mit Tailwind CSS
- Datenbank: SQLite für lokale Konfigurationsspeicherung

## Deployment

Die Anwendung kann auf zwei Arten deployed werden:

### 1. Docker (empfohlen)

```bash
docker-compose up --build
```

### 2. Manuelle Installation

1. Frontend bauen:
```bash
npm run build
```

2. Nginx konfigurieren:
- Kopiere die `nginx.conf` in `/etc/nginx/nginx.conf`
- Kopiere den Build-Output aus `dist` nach `/var/www/html`

3. Backend starten:
```bash
uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
```

## Konfiguration

### Neue Drucker hinzufügen

1. Erstelle einen neuen Ordner unter `config/` mit dem Druckernamen
2. Füge `printer.cfg` und `firmware.config` hinzu
3. Aktualisiere `printer_metadata.json` mit den Druckerinformationen

### Umgebungsvariablen

- `KLIPPER_INSTALLER_ENV`: Entwicklungsumgebung (development/production)
- `LOG_LEVEL`: Logging-Level (DEBUG/INFO/WARNING/ERROR)

## Lizenz

MIT
