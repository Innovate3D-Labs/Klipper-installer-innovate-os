# Klipper Installer für InnovateOS

Ein einfacher Installer für Klipper auf deinem 3D-Drucker.

## Installation

1. Repository klonen:
```bash
git clone https://github.com/Innovate3D-Labs/Klipper-installer-innovate-os.git
cd Klipper-installer-innovate-os
```

2. Installer starten:
```bash
chmod +x start.sh
./start.sh
```

## Verwendung

1. Öffne im Browser:
```
http://localhost:8000
```

2. Folge dem Setup-Assistenten:
   - Wähle deinen 3D-Drucker aus
   - Konfiguriere die Firmware
   - Starte die Installation

## Unterstützte Drucker

- Ender 3 (alle Varianten)
- Ratrig VCore 3
- Voron 2.4
- Voron Trident
- (weitere folgen)

## Probleme?

### USB-Port nicht gefunden
```bash
sudo usermod -a -G dialout $USER
sudo reboot
```

### Dienst neu starten
```bash
sudo systemctl restart klipper
```

### Logs anzeigen
```bash
tail -f /var/log/klipper/klipper.log
```

## Support

Bei Problemen oder Fragen:
- Öffne ein Issue auf GitHub
- Besuche unser [Forum](https://forum.innovate3d.de)
- Discord: [Innovate3D Community](https://discord.gg/innovate3d)
