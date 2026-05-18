from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, room_id: str, username: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
        self.rooms[room_id][username] = websocket
        await self.broadcast(room_id, {
            "type": "system",
            "text": f"{username} joined the room"
        })

    def disconnect(self, room_id: str, username: str):
        if room_id in self.rooms and username in self.rooms[room_id]:
            del self.rooms[room_id][username]
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def broadcast(self, room_id: str, payload: dict):
        if room_id not in self.rooms:
            return
        for ws in self.rooms[room_id].values():
            try:
                await ws.send_json(payload)
            except:
                pass

    def get_users(self, room_id: str) -> list:
        if room_id not in self.rooms:
            return []
        return list(self.rooms[room_id].keys())

room_manager = RoomManager()    