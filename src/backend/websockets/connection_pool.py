from typing import Dict, Optional
from fastapi import WebSocket
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionPool:
    def __init__(self):
        self._connections: Dict[str, WebSocket] = {}
        self._message_count = 0
        self._last_activity = datetime.now()

    def add_connection(self, client_id: str, websocket: WebSocket) -> None:
        """Fügt eine neue Verbindung zum Pool hinzu"""
        self._connections[client_id] = websocket
        self._last_activity = datetime.now()

    def remove_connection(self, client_id: str) -> None:
        """Entfernt eine Verbindung aus dem Pool"""
        if client_id in self._connections:
            del self._connections[client_id]
            self._last_activity = datetime.now()

    def get_connection(self, client_id: str) -> Optional[WebSocket]:
        """Gibt die WebSocket-Verbindung für einen Client zurück"""
        return self._connections.get(client_id)

    async def send_to_client(self, client_id: str, message: dict) -> bool:
        """Sendet eine Nachricht an einen spezifischen Client"""
        if client_id in self._connections:
            try:
                await self._connections[client_id].send_json(message)
                self._message_count += 1
                self._last_activity = datetime.now()
                return True
            except Exception as e:
                logger.error(f"Error sending message to client {client_id}: {str(e)}")
                self.remove_connection(client_id)
        return False

    async def broadcast(self, message: dict) -> None:
        """Sendet eine Nachricht an alle Clients im Pool"""
        disconnected_clients = []
        
        for client_id, websocket in self._connections.items():
            try:
                await websocket.send_json(message)
                self._message_count += 1
            except Exception as e:
                logger.error(f"Error broadcasting to client {client_id}: {str(e)}")
                disconnected_clients.append(client_id)

        # Entferne getrennte Verbindungen
        for client_id in disconnected_clients:
            self.remove_connection(client_id)

        if len(disconnected_clients) > 0:
            self._last_activity = datetime.now()

    def is_empty(self) -> bool:
        """Prüft, ob der Pool leer ist"""
        return len(self._connections) == 0

    def get_stats(self) -> dict:
        """Gibt Statistiken für den Pool zurück"""
        return {
            "connected_clients": len(self._connections),
            "message_count": self._message_count,
            "last_activity": self._last_activity.isoformat()
        }
