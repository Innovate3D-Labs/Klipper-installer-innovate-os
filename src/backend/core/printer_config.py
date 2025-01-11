from typing import List, Dict, Optional
from pydantic import BaseModel
import os
import json

class PrinterConfig(BaseModel):
    name: str
    model: str
    config_path: str
    firmware_path: Optional[str] = None
    description: Optional[str] = None

class PrinterConfigManager:
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.printers: Dict[str, PrinterConfig] = {}
        self._load_configs()

    def _load_configs(self):
        """Lädt alle verfügbaren Druckerkonfigurationen"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            return

        for printer_dir in os.listdir(self.config_dir):
            config_path = os.path.join(self.config_dir, printer_dir, "printer.cfg")
            firmware_path = os.path.join(self.config_dir, printer_dir, "firmware.config")
            
            if os.path.exists(config_path):
                self.printers[printer_dir] = PrinterConfig(
                    name=printer_dir,
                    model=printer_dir.replace("_", " ").title(),
                    config_path=config_path,
                    firmware_path=firmware_path if os.path.exists(firmware_path) else None
                )

    def get_all_printers(self) -> List[PrinterConfig]:
        """Gibt eine Liste aller verfügbaren Drucker zurück"""
        return list(self.printers.values())

    def get_printer_config(self, printer_name: str) -> Optional[PrinterConfig]:
        """Gibt die Konfiguration für einen bestimmten Drucker zurück"""
        return self.printers.get(printer_name)
