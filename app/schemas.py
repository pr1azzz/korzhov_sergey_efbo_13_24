from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=80)
    description: Optional[str] = None
    status: str = Field(..., pattern="^(todo|in_progress|done)$")
    priority: int = Field(..., ge=1, le=5)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: int
    owner_id: int

class TaskStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(todo|in_progress|done)$")

class User(BaseModel):
    id: int
    role: str

class WebSocketMessage(BaseModel):
    type: str
    text: Optional[str] = None
    room_id: Optional[str] = None
    username: Optional[str] = None
    detail: Optional[str] = None