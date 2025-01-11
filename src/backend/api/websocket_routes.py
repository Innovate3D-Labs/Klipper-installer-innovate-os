from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from ..websockets.connection_manager import manager
from ..core.auth import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    try:
        await manager.connect(websocket, client_id)
        
        # Sende initiale Bestätigung
        await websocket.send_json({
            "type": "connection_established",
            "data": {
                "client_id": client_id,
                "message": "WebSocket Verbindung hergestellt"
            }
        })
        
        while True:
            try:
                # Empfange Nachrichten vom Client
                data = await websocket.receive_json()
                
                # Verarbeite verschiedene Nachrichtentypen
                if data.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "data": {"timestamp": data.get("timestamp")}
                    })
                    
                elif data.get("type") == "subscribe":
                    # Hier könnte eine Subscription-Logik implementiert werden
                    pass
                    
            except WebSocketDisconnect:
                manager.disconnect(websocket, client_id)
                break
                
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
                await manager.broadcast_error(
                    "Fehler bei der Verarbeitung der WebSocket Nachricht",
                    str(e),
                    client_id
                )
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        try:
            await websocket.close()
        except:
            pass
