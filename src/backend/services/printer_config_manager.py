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
        # Suche nach angeschlossenen USB-Druckern
        ports = list(serial.tools.list_ports.comports())
        printers = []
        
        for port in ports:
            # Füge jeden gefundenen USB-Port als möglichen Drucker hinzu
            printer_info = {
                "id": port.device,
                "name": f"3D Drucker ({port.device})",
                "port": port.device,
                "description": port.description,
                "manufacturer": port.manufacturer if hasattr(port, 'manufacturer') else None,
                "hardware_id": port.hwid if hasattr(port, 'hwid') else None,
                "status": "connected"
            }
            printers.append(printer_info)
            
        return printers

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
                # Update nur die angegebenen Felder
                printer.update(printer_data)

                # Aktualisiere die Konfiguration wenn vorhanden
                if "config" in printer_data:
                    config_path = os.path.join(self.config_dir, printer["config_dir"], "printer.cfg")
                    with open(config_path, 'w') as f:
                        f.write(printer_data["config"])

                self._save_metadata()
                return printer
        return None

    def delete_printer_config(self, printer_id: str) -> bool:
        """Löscht eine Druckerkonfiguration"""
        for i, printer in enumerate(self.metadata["printers"]):
            if printer.get("id") == printer_id:
                # Lösche das Konfigurationsverzeichnis
                config_dir = os.path.join(self.config_dir, printer["config_dir"])
                if os.path.exists(config_dir):
                    import shutil
                    shutil.rmtree(config_dir)

                # Entferne den Drucker aus der Metadata
                self.metadata["printers"].pop(i)
                self._save_metadata()
                return True
        return False
