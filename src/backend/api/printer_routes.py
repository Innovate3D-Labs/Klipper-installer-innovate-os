from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from ..services.printer_config_manager import PrinterConfigManager
from ..core.schemas import PrinterConfig, PrinterResponse, PrinterCreate, PrinterUpdate

router = APIRouter()
config_manager = PrinterConfigManager()

@router.get("/printers", response_model=List[PrinterResponse])
async def get_printers():
    """Gibt eine Liste aller verfügbaren Drucker zurück"""
    return config_manager.get_available_printers()

@router.get("/printers/{printer_id}", response_model=PrinterResponse)
async def get_printer(printer_id: str):
    """Holt die Details eines bestimmten Druckers"""
    printer = config_manager.get_printer_config(printer_id)
    if not printer:
        raise HTTPException(status_code=404, detail="Drucker nicht gefunden")
    return printer

@router.post("/printers", response_model=PrinterResponse)
async def create_printer(printer: PrinterCreate):
    """Erstellt eine neue Druckerkonfiguration"""
    try:
        if printer.config and not config_manager.validate_config(printer.config):
            raise HTTPException(
                status_code=400, 
                detail="Ungültige Druckerkonfiguration"
            )
        
        return config_manager.add_printer_config(printer.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interner Server-Fehler: {str(e)}")

@router.put("/printers/{printer_id}", response_model=PrinterResponse)
async def update_printer(printer_id: str, printer: PrinterUpdate):
    """Aktualisiert eine bestehende Druckerkonfiguration"""
    try:
        if printer.config and not config_manager.validate_config(printer.config):
            raise HTTPException(
                status_code=400,
                detail="Ungültige Druckerkonfiguration"
            )
        
        updated_printer = config_manager.update_printer_config(printer_id, printer.dict(exclude_unset=True))
        if not updated_printer:
            raise HTTPException(status_code=404, detail="Drucker nicht gefunden")
        return updated_printer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Interner Server-Fehler: {str(e)}")

@router.delete("/printers/{printer_id}")
async def delete_printer(printer_id: str):
    """Löscht eine Druckerkonfiguration"""
    if not config_manager.delete_printer_config(printer_id):
        raise HTTPException(status_code=404, detail="Drucker nicht gefunden")
    return {"message": "Drucker erfolgreich gelöscht"}
