from fastapi import APIRouter, Depends, HTTPException
from ..core.schemas import Settings, SettingsUpdate
from ..services.settings_manager import SettingsManager
from ..core.auth import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
settings_manager = SettingsManager()

@router.get("/settings", response_model=Settings)
async def get_settings():
    """
    Aktuelle Einstellungen abrufen
    """
    try:
        return await settings_manager.get_settings()
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/settings", response_model=Settings)
async def update_settings(settings: SettingsUpdate):
    """
    Einstellungen aktualisieren
    """
    try:
        return await settings_manager.update_settings(settings)
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/settings/backup")
async def create_backup():
    """
    Backup der aktuellen Konfiguration erstellen
    """
    try:
        backup_path = await settings_manager.create_backup()
        return {"message": "Backup erfolgreich erstellt", "path": backup_path}
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/settings/restore/{backup_id}")
async def restore_backup(backup_id: str):
    """
    Konfiguration aus Backup wiederherstellen
    """
    try:
        await settings_manager.restore_backup(backup_id)
        return {"message": "Backup erfolgreich wiederhergestellt"}
    except Exception as e:
        logger.error(f"Error restoring backup: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/settings/backups")
async def list_backups():
    """
    Liste aller verfügbaren Backups abrufen
    """
    try:
        backups = await settings_manager.list_backups()
        return {"backups": backups}
    except Exception as e:
        logger.error(f"Error listing backups: {e}")
        raise HTTPException(status_code=500, detail=str(e))
