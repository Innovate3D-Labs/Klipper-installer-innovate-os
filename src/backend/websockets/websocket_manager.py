from typing import Dict, List, Optional
from fastapi import WebSocket
import logging
import asyncio
import json
from datetime import datetime
from .connection_pool import ConnectionPool

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self._pools: Dict[str, ConnectionPool] = {}
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._batch_size = 10
        self._batch_timeout = 0.1  # 100ms
        asyncio.create_task(self._process_message_queue())

    async def connect(self, websocket: WebSocket, client_id: str, pool_id: str = "default"):
        """Verbindet einen WebSocket-Client"""
        await websocket.accept()
        
        if pool_id not in self._pools:
            self._pools[pool_id] = ConnectionPool()
        
        self._pools[pool_id].add_connection(client_id, websocket)
        logger.info(f"Client {client_id} connected to pool {pool_id}")

    def disconnect(self, client_id: str, pool_id: str = "default"):
        """Trennt einen WebSocket-Client"""
        if pool_id in self._pools:
            self._pools[pool_id].remove_connection(client_id)
            if self._pools[pool_id].is_empty():
                del self._pools[pool_id]
        logger.info(f"Client {client_id} disconnected from pool {pool_id}")

    async def broadcast(self, message: dict, pool_id: str = "default"):
        """Sendet eine Nachricht an alle Clients in einem Pool"""
        await self._message_queue.put((pool_id, None, message))

    async def send_to_client(self, client_id: str, message: dict, pool_id: str = "default"):
        """Sendet eine Nachricht an einen bestimmten Client"""
        await self._message_queue.put((pool_id, client_id, message))

    async def _process_message_queue(self):
        """Verarbeitet die Nachrichten-Warteschlange in Batches"""
        while True:
            messages = []
            try:
                # Sammle Nachrichten für den aktuellen Batch
                while len(messages) < self._batch_size:
                    try:
                        message = await asyncio.wait_for(
                            self._message_queue.get(),
                            timeout=self._batch_timeout
                        )
                        messages.append(message)
                    except asyncio.TimeoutError:
                        break

                if not messages:
                    continue

                # Gruppiere Nachrichten nach Pool
                pool_messages: Dict[str, List] = {}
                for pool_id, client_id, message in messages:
                    if pool_id not in pool_messages:
                        pool_messages[pool_id] = []
                    pool_messages[pool_id].append((client_id, message))

                # Sende Nachrichten für jeden Pool
                for pool_id, pool_msgs in pool_messages.items():
                    if pool_id in self._pools:
                        pool = self._pools[pool_id]
                        for client_id, message in pool_msgs:
                            if client_id:
                                # Sende an spezifischen Client
                                await pool.send_to_client(client_id, message)
                            else:
                                # Broadcast an alle Clients im Pool
                                await pool.broadcast(message)

            except Exception as e:
                logger.error(f"Error processing message queue: {str(e)}")
                await asyncio.sleep(1)  # Verhindere CPU-Überlastung bei Fehlern

    def get_pool_stats(self, pool_id: str = "default") -> dict:
        """Gibt Statistiken für einen Pool zurück"""
        if pool_id in self._pools:
            return self._pools[pool_id].get_stats()
        return {"connected_clients": 0, "message_count": 0}

# Globale WebSocket-Manager-Instanz
websocket_manager = WebSocketManager()
