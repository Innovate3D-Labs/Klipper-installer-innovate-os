from typing import Dict, List
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)
        logger.info(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket, client_id: str):
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
        logger.info(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")

    async def send_message(self, message: dict, client_id: str = None):
        """
        Sendet eine Nachricht an einen bestimmten Client oder an alle Clients
        """
        if client_id:
            if client_id in self.active_connections:
                for connection in self.active_connections[client_id]:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        logger.error(f"Error sending message to client {client_id}: {e}")
        else:
            for client_connections in self.active_connections.values():
                for connection in client_connections:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        logger.error(f"Error broadcasting message: {e}")

    async def broadcast_installation_progress(self, step: str, progress: float, message: str, client_id: str = None):
        """
        Sendet Installations-Fortschritt an Clients
        """
        message = {
            "type": "installation_progress",
            "data": {
                "step": step,
                "progress": progress,
                "message": message
            }
        }
        await self.send_message(message, client_id)

    async def broadcast_printer_status(self, printer_id: str, status: dict, client_id: str = None):
        """
        Sendet Drucker-Status-Updates an Clients
        """
        message = {
            "type": "printer_status",
            "data": {
                "printer_id": printer_id,
                "status": status
            }
        }
        await self.send_message(message, client_id)

    async def broadcast_error(self, error_message: str, details: str = None, client_id: str = None):
        """
        Sendet Fehlermeldungen an Clients
        """
        message = {
            "type": "error",
            "data": {
                "message": error_message,
                "details": details
            }
        }
        await self.send_message(message, client_id)

manager = ConnectionManager()
