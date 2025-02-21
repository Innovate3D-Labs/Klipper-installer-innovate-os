import os
import json
import serial.tools.list_ports
from typing import List, Dict, Optional
from pathlib import Path

class PrinterConfigManager:
    def __init__(self, config_dir: str = "config"):
        """Initialisiert den PrinterConfigManager"""
        self.config_dir = config_dir
        self.metadata_file = os.path.join(config_dir, "printer_metadata.json")
        self._ensure_config_dir()
        self._load_metadata()

    def _ensure_config_dir(self):
        """Stellt sicher, dass das Konfigurationsverzeichnis existiert"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        if not os.path.exists(self.metadata_file):
            self._create_default_metadata()

    def _create_default_metadata(self):
        """Erstellt eine Standard-Metadata-Datei"""
        default_metadata = {
            "printers": []
        }
        with open(self.metadata_file, 'w') as f:
            json.dump(default_metadata, f, indent=2)

    def _load_metadata(self):
        """Lädt die Drucker-Metadaten"""
        try:
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden der Metadaten: {e}")
            self.metadata = {"printers": []}

    def _save_metadata(self):
        """Speichert die Drucker-Metadaten"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def get_available_printers(self) -> List[Dict]:
        """Gibt eine Liste aller verfügbaren Drucker zurück"""
        try:
            # Debug: Zeige alle verfügbaren Ports
            print("Suche nach verfügbaren USB-Ports...")
            ports = list(serial.tools.list_ports.comports())
            print(f"Gefundene Ports: {len(ports)}")
            
            printers = []
            
            for port in ports:
                # Debug: Zeige Details für jeden Port
                print(f"\nPort gefunden:")
                print(f"  Device: {port.device}")
                print(f"  Name: {port.name if hasattr(port, 'name') else 'N/A'}")
                print(f"  Description: {port.description}")
                print(f"  HWID: {port.hwid if hasattr(port, 'hwid') else 'N/A'}")
                print(f"  VID:PID: {port.vid if hasattr(port, 'vid') else 'N/A'}:{port.pid if hasattr(port, 'pid') else 'N/A'}")
                print(f"  Serial Number: {port.serial_number if hasattr(port, 'serial_number') else 'N/A'}")
                print(f"  Location: {port.location if hasattr(port, 'location') else 'N/A'}")
                print(f"  Manufacturer: {port.manufacturer if hasattr(port, 'manufacturer') else 'N/A'}")
                print(f"  Product: {port.product if hasattr(port, 'product') else 'N/A'}")
                print(f"  Interface: {port.interface if hasattr(port, 'interface') else 'N/A'}")
                
                # Füge jeden gefundenen USB-Port als möglichen Drucker hinzu
                printer_info = {
                    "id": port.device,
                    "name": port.description or f"3D Drucker ({port.device})",
                    "port": port.device,
                    "description": port.description,
                    "manufacturer": port.manufacturer if hasattr(port, 'manufacturer') else None,
                    "hardware_id": port.hwid if hasattr(port, 'hwid') else None,
                    "vid": port.vid if hasattr(port, 'vid') else None,
                    "pid": port.pid if hasattr(port, 'pid') else None,
                    "serial_number": port.serial_number if hasattr(port, 'serial_number') else None,
                    "status": "connected"
                }
                printers.append(printer_info)
            
            # Debug: Zeige gefundene Drucker
            print(f"\nGefundene Drucker: {len(printers)}")
            for printer in printers:
                print(f"  - {printer['name']} ({printer['port']})")
            
            return printers
            
        except Exception as e:
            print(f"Fehler beim Suchen nach Druckern: {str(e)}")
            return []

    def get_printer_config(self, printer_id: str) -> Optional[Dict]:
        """Holt die Konfiguration für einen bestimmten Drucker"""
        for printer in self.metadata.get("printers", []):
            if printer.get("id") == printer_id:
                config_path = os.path.join(self.config_dir, printer.get("config_dir"), "printer.cfg")
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        printer["config"] = f.read()
                return printer
        return None

    def validate_config(self, config: str) -> bool:
        """Validiert eine Druckerkonfiguration"""
        # TODO: Implementiere Konfigurationsvalidierung
        return True

    def add_printer_config(self, printer_data: Dict) -> Dict:
        """Fügt eine neue Druckerkonfiguration hinzu"""
        # Generiere eine eindeutige ID falls keine vorhanden
        if "id" not in printer_data:
            printer_data["id"] = str(len(self.metadata["printers"]) + 1)

        # Erstelle ein Verzeichnis für die Druckerkonfiguration
        config_dir = f"printer_{printer_data['id']}"
        printer_data["config_dir"] = config_dir
        os.makedirs(os.path.join(self.config_dir, config_dir), exist_ok=True)

        # Speichere die Konfiguration wenn vorhanden
        if "config" in printer_data:
            config_path = os.path.join(self.config_dir, config_dir, "printer.cfg")
            with open(config_path, 'w') as f:
                f.write(printer_data["config"])

        # Füge den Drucker zur Metadata hinzu
        self.metadata["printers"].append(printer_data)
        self._save_metadata()
        return printer_data

    def update_printer_config(self, printer_id: str, printer_data: Dict) -> Optional[Dict]:
        """Aktualisiert eine bestehende Druckerkonfiguration"""
        for i, printer in enumerate(self.metadata["printers"]):
            if printer.get("id") == printer_id:
                # Update die Konfiguration wenn vorhanden
                if "config" in printer_data:
                    config_path = os.path.join(self.config_dir, printer.get("config_dir"), "printer.cfg")
                    with open(config_path, 'w') as f:
                        f.write(printer_data["config"])

                # Update die Metadaten
                self.metadata["printers"][i].update(printer_data)
                self._save_metadata()
                return self.metadata["printers"][i]
        return None

    def delete_printer_config(self, printer_id: str) -> bool:
        """Löscht eine Druckerkonfiguration"""
        for i, printer in enumerate(self.metadata["printers"]):
            if printer.get("id") == printer_id:
                # Lösche das Konfigurationsverzeichnis
                config_dir = os.path.join(self.config_dir, printer.get("config_dir"))
                if os.path.exists(config_dir):
                    import shutil
                    shutil.rmtree(config_dir)

                # Entferne den Drucker aus den Metadaten
                self.metadata["printers"].pop(i)
                self._save_metadata()
                return True
        return False
