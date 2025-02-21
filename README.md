# Klipper Installer für InnovateOS

Ein benutzerfreundlicher Installer für Klipper 3D-Drucker Firmware, entwickelt für InnovateOS.

## Features

- 🔍 Automatische USB-Drucker Erkennung
- 🛠️ Einfache Klipper Installation
- ⚙️ Automatische Firmware-Kompilierung
- 📱 Moderne Web-Oberfläche
- 🔄 Echtzeit-Installation-Status
- 📊 Detaillierte Fortschrittsanzeige

## Systemanforderungen

- Python 3.11+
- Node.js 18+
- Linux/Raspberry Pi OS
- Git

## Installation

1. Repository klonen:
```bash
git clone https://github.com/Innovate3D-Labs/Klipper-installer-innovate-os.git
cd Klipper-installer-innovate-os
```

2. Python-Abhängigkeiten installieren:
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Frontend-Abhängigkeiten installieren:
```bash
cd src/frontend
npm install
```

## Entwicklung

1. Backend-Server starten:
```bash
python -m uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000
```

2. Frontend-Development-Server starten:
```bash
cd src/frontend
npm run dev
```

## Produktions-Build

1. Frontend bauen:
```bash
cd src/frontend
npm run build
```

2. Backend-Server starten:
```bash
python -m uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
```

## Unterstützte Drucker

- Alle Drucker mit RAMPS 1.4 Board
- Weitere Boards werden in zukünftigen Updates hinzugefügt

## Lizenz

MIT License

## Beitragen

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request
