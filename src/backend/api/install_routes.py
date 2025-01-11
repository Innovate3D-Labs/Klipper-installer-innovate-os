from fastapi import APIRouter, WebSocket, HTTPException
from typing import Dict
import asyncio
from ..services.klipper_installer import KlipperInstaller
from ..core.printer_config import PrinterConfigManager

router = APIRouter()
installer = KlipperInstaller()
config_manager = PrinterConfigManager()

@router.websocket("/ws/install/{printer_name}")
async def install_websocket(websocket: WebSocket, printer_name: str):
    await websocket.accept()
    
    # Callback für Statusupdates
    async def status_callback(status: Dict):
        await websocket.send_json(status)
    
    installer.set_status_callback(status_callback)
    
    try:
        printer_config = config_manager.get_printer_config(printer_name)
        if not printer_config:
            raise HTTPException(status_code=404, detail="Drucker nicht gefunden")
        
        # Installation starten
        await installer.install_dependencies()
        await installer.clone_klipper()
        
        if printer_config.firmware_path:
            await installer.compile_firmware(printer_config.firmware_path)
            
        await installer.install_service()
        
        await websocket.send_json({
            "status": "completed",
            "message": "Installation erfolgreich abgeschlossen"
        })
        
    except Exception as e:
        await websocket.send_json({
            "status": "error",
            "error": str(e)
        })
    finally:
        await websocket.close()
