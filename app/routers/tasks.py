from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from app.schemas import TaskCreate, TaskResponse, TaskStatusUpdate
from app.dependencies import get_current_user, get_storage
from app.storage import TaskStorage

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    current_user=Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    task_data = task.model_dump()
    task_data["owner_id"] = current_user.id
    return storage.create(task_data)

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[str] = Query(None),
    min_priority: Optional[int] = Query(None, ge=1, le=5),
    current_user=Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    tasks = storage.get_all()
    tasks = [t for t in tasks if t["owner_id"] == current_user.id]
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if min_priority:
        tasks = [t for t in tasks if t["priority"] >= min_priority]
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user=Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    update: TaskStatusUpdate,
    current_user=Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = storage.update_status(task_id, update.status)
    return updated

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    current_user=Depends(get_current_user),
    storage: TaskStorage = Depends(get_storage)
):
    task = storage.get_by_id(task_id)
    if not task or task["owner_id"] != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    storage.delete(task_id)