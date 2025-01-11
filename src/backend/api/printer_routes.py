from fastapi import APIRouter, HTTPException
from typing import List
from ..core.printer_config import PrinterConfigManager, PrinterConfig

router = APIRouter()
config_manager = PrinterConfigManager()

@router.get("/printers", response_model=List[PrinterConfig])
async def get_printers():
    """Liste aller verfügbaren Drucker abrufen"""
    return config_manager.get_all_printers()

@router.get("/printers/{printer_name}", response_model=PrinterConfig)
async def get_printer(printer_name: str):
    """Details eines spezifischen Druckers abrufen"""
    printer = config_manager.get_printer_config(printer_name)
    if not printer:
        raise HTTPException(status_code=404, detail="Drucker nicht gefunden")
    return printer
