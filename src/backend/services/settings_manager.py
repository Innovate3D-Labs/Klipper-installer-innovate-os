import os
import json
import shutil
from datetime import datetime
from typing import List, Dict, Optional
from ..core.schemas import Settings, SettingsUpdate
import logging

logger = logging.getLogger(__name__)

class SettingsManager:
    def __init__(self):
        self.settings_file = "config/settings.json"
        self.backups_dir = "config/backups"
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Stellt sicher, dass alle benötigten Verzeichnisse existieren"""
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        os.makedirs(self.backups_dir, exist_ok=True)

    async def get_settings(self) -> Settings:
        """Aktuelle Einstellungen laden"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return Settings(**json.load(f))
            return Settings(
                language="de",
                theme="light",
                auto_update=True,
                debug_mode=False
            )
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            raise

    async def update_settings(self, settings: SettingsUpdate) -> Settings:
        """Einstellungen aktualisieren"""
        try:
            current_settings = await self.get_settings()
            updated_settings = current_settings.copy(update=settings.dict(exclude_unset=True))
            
            with open(self.settings_file, 'w') as f:
                json.dump(updated_settings.dict(), f, indent=2)
            
            return updated_settings
        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            raise

    async def create_backup(self) -> str:
        """
        Erstellt ein Backup der aktuellen Konfiguration
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = os.path.join(self.backups_dir, f"backup_{timestamp}")
            os.makedirs(backup_dir)

            # Kopiere Konfigurationsdateien
            config_files = [
                "config/settings.json",
                "config/printers.json",
                "config/interfaces.json"
            ]

            for file in config_files:
                if os.path.exists(file):
                    shutil.copy2(file, backup_dir)

            # Erstelle Backup-Info
            backup_info = {
                "timestamp": timestamp,
                "files": config_files,
                "version": "1.0"
            }
            
            with open(os.path.join(backup_dir, "backup_info.json"), 'w') as f:
                json.dump(backup_info, f, indent=2)

            return backup_dir
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            raise

    async def restore_backup(self, backup_id: str):
        """
        Stellt eine Konfiguration aus einem Backup wieder her
        """
        try:
            backup_dir = os.path.join(self.backups_dir, backup_id)
            if not os.path.exists(backup_dir):
                raise ValueError(f"Backup {backup_id} nicht gefunden")

            # Lade Backup-Info
            with open(os.path.join(backup_dir, "backup_info.json"), 'r') as f:
                backup_info = json.load(f)

            # Stelle Dateien wieder her
            for file in backup_info["files"]:
                backup_file = os.path.join(backup_dir, os.path.basename(file))
                if os.path.exists(backup_file):
                    shutil.copy2(backup_file, file)

        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            raise

    async def list_backups(self) -> List[Dict]:
        """
        Liste aller verfügbaren Backups
        """
        try:
            backups = []
            for backup_dir in os.listdir(self.backups_dir):
                info_file = os.path.join(self.backups_dir, backup_dir, "backup_info.json")
                if os.path.exists(info_file):
                    with open(info_file, 'r') as f:
                        info = json.load(f)
                        backups.append({
                            "id": backup_dir,
                            "timestamp": info["timestamp"],
                            "version": info["version"],
                            "files": info["files"]
                        })
            return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            raise
