from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.analysis_updates: Dict = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def update_analysis_progress(self, analysis_id: str, progress: int, message: str):
        update = {
            "analysis_id": analysis_id,
            "progress": progress,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.analysis_updates[analysis_id] = update
        await self.broadcast(json.dumps(update))

manager = ConnectionManager()

async def handle_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)