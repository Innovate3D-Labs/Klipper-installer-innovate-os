from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.interface_manager import InterfaceManager

router = APIRouter()
interface_manager = InterfaceManager()

class InterfaceRequest(BaseModel):
    interface: str

@router.get("/interfaces/current")
async def get_current_interface():
    """Gibt die aktuell installierte Weboberfläche zurück"""
    current = interface_manager.get_current_interface()
    return {"current_interface": current}

@router.post("/interfaces/switch")
async def switch_interface(request: InterfaceRequest):
    """Wechselt zwischen Fluidd und Mainsail"""
    try:
        success = await interface_manager.switch_interface(request.interface)
        if success:
            return {"message": f"Erfolgreich zu {request.interface} gewechselt"}
        else:
            raise HTTPException(status_code=500, detail="Fehler beim Wechsel der Weboberfläche")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
