from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from app.routers import tasks, users, admin
from app.websocket.room_manager import room_manager
from app.schemas import WebSocketMessage
from app.storage import storage

app = FastAPI(title="Task Manager API")

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(admin.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.websocket("/ws/rooms/{room_id}")
async def websocket_room(websocket: WebSocket, room_id: str, username: str = None):
    if not username or not username.strip():
        await websocket.close(code=1008)
        return
    username = username.strip()
    
    await room_manager.connect(room_id, username, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")
            text = data.get("text", "")
            
            if msg_type == "message":
                if len(text) > 300:
                    await websocket.send_json({
                        "type": "error",
                        "detail": "Message is too long"
                    })
                else:
                    await room_manager.broadcast(room_id, {
                        "type": "message",
                        "room_id": room_id,
                        "username": username,
                        "text": text
                    })
    except WebSocketDisconnect:
        room_manager.disconnect(room_id, username)
        await room_manager.broadcast(room_id, {
            "type": "system",
            "text": f"{username} left the room"
        })

@app.get("/rooms/{room_id}/users")
def get_room_users(room_id: str):
    return {"room_id": room_id, "users": room_manager.get_users(room_id)}