# Klipper Installer für InnovateOS

Ein einfacher Installer für Klipper auf deinem 3D-Drucker.

## Installation

1. Lade das neueste Release herunter:
```bash
wget https://github.com/Innovate3D-Labs/Klipper-installer-innovate-os/releases/latest/download/klipper-installer.sh
```

2. Mache das Script ausführbar:
```bash
chmod +x klipper-installer.sh
```

3. Führe den Installer aus:
```bash
./klipper-installer.sh
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
