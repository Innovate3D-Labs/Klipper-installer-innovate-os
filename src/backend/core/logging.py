import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Optional

class KlipperLogger:
    _instance: Optional['KlipperLogger'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KlipperLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Initialisiert den Logger mit Datei- und Konsolenausgabe"""
        self.logger = logging.getLogger('klipper_installer')
        self.logger.setLevel(logging.DEBUG)

        # Erstelle logs Verzeichnis falls nicht vorhanden
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Datei-Handler mit Rotation
        log_file = os.path.join(log_dir, 'klipper_installer.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        # Konsolen-Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)

        # Handler hinzufügen
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """Gibt die Logger-Instanz zurück"""
        return self.logger

    @staticmethod
    def format_error(error: Exception) -> str:
        """Formatiert einen Fehler für das Logging"""
        return f"{type(error).__name__}: {str(error)}"

class LogEntry:
    def __init__(self, level: str, message: str, timestamp: Optional[datetime] = None):
        self.level = level
        self.message = message
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        return {
            'level': self.level,
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }

class InstallationLogger:
    def __init__(self):
        self.logger = KlipperLogger().get_logger()
        self.installation_logs: list[LogEntry] = []

    def log(self, level: str, message: str):
        """Fügt einen Log-Eintrag hinzu"""
        log_entry = LogEntry(level, message)
        self.installation_logs.append(log_entry)
        
        # Logging an den Haupt-Logger weiterleiten
        if level == 'ERROR':
            self.logger.error(message)
        elif level == 'WARNING':
            self.logger.warning(message)
        else:
            self.logger.info(message)

    def get_logs(self) -> list[dict]:
        """Gibt alle Log-Einträge zurück"""
        return [log.to_dict() for log in self.installation_logs]

    def clear_logs(self):
        """Löscht alle Log-Einträge"""
        self.installation_logs.clear()

# Globale Logger-Instanz
logger = KlipperLogger().get_logger()
