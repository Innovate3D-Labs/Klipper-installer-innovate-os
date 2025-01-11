import os
import json
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
        return self.metadata.get("printers", [])

    def get_printer_config(self, printer_id: str) -> Optional[Dict]:
        """Holt die Konfiguration für einen bestimmten Drucker"""
        for printer in self.metadata.get("printers", []):
            if printer.get("id") == printer_id:
                config_path = os.path.join(self.config_dir, printer.get("config_dir"), "printer.cfg")
                if os.path.exists(config_path):
                    with open(config_path, 'r') as f:
                        config_content = f.read()
                    return {
                        **printer,
                        "config": config_content
                    }
        return None

    def add_printer_config(self, printer_data: Dict) -> Dict:
        """Fügt eine neue Druckerkonfiguration hinzu"""
        required_fields = ["id", "name", "manufacturer", "type"]
        for field in required_fields:
            if field not in printer_data:
                raise ValueError(f"Fehlendes Pflichtfeld: {field}")

        # Erstelle Verzeichnis für die Druckerkonfiguration
        config_dir = os.path.join(self.config_dir, printer_data["id"])
        os.makedirs(config_dir, exist_ok=True)

        # Speichere Konfigurationsdatei
        if "config" in printer_data:
            config_path = os.path.join(config_dir, "printer.cfg")
            with open(config_path, 'w') as f:
                f.write(printer_data["config"])
            del printer_data["config"]

        # Aktualisiere Metadata
        printer_data["config_dir"] = printer_data["id"]
        self.metadata["printers"].append(printer_data)
        self._save_metadata()

        return printer_data

    def update_printer_config(self, printer_id: str, printer_data: Dict) -> Optional[Dict]:
        """Aktualisiert eine bestehende Druckerkonfiguration"""
        for i, printer in enumerate(self.metadata.get("printers", [])):
            if printer.get("id") == printer_id:
                # Update Konfigurationsdatei wenn vorhanden
                if "config" in printer_data:
                    config_path = os.path.join(self.config_dir, printer["config_dir"], "printer.cfg")
                    with open(config_path, 'w') as f:
                        f.write(printer_data["config"])
                    del printer_data["config"]

                # Update Metadata
                updated_printer = {**printer, **printer_data}
                self.metadata["printers"][i] = updated_printer
                self._save_metadata()
                return updated_printer
        return None

    def delete_printer_config(self, printer_id: str) -> bool:
        """Löscht eine Druckerkonfiguration"""
        for i, printer in enumerate(self.metadata.get("printers", [])):
            if printer.get("id") == printer_id:
                # Lösche Konfigurationsverzeichnis
                config_dir = os.path.join(self.config_dir, printer["config_dir"])
                if os.path.exists(config_dir):
                    for root, dirs, files in os.walk(config_dir, topdown=False):
                        for name in files:
                            os.remove(os.path.join(root, name))
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                    os.rmdir(config_dir)

                # Update Metadata
                self.metadata["printers"].pop(i)
                self._save_metadata()
                return True
        return False

    def validate_config(self, config_content: str) -> bool:
        """Validiert eine Druckerkonfiguration"""
        # TODO: Implementiere Konfigurationsvalidierung
        required_sections = ["printer", "stepper_x", "stepper_y", "stepper_z", "extruder"]
        
        # Einfache Syntax-Überprüfung
        try:
            lines = config_content.split('\n')
            sections = [line.strip('[].') for line in lines if line.strip().startswith('[')]
            
            # Prüfe ob alle erforderlichen Sektionen vorhanden sind
            for required in required_sections:
                if not any(section.startswith(required) for section in sections):
                    return False
                    
            return True
        except Exception:
            return False
