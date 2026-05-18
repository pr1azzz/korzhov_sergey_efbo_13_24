from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import require_admin, get_storage
from collections import Counter

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats")
def get_stats(admin=Depends(require_admin), storage=Depends(get_storage)):
    tasks = storage.get_all()
    by_status = Counter(t["status"] for t in tasks)
    return {
        "total_tasks": len(tasks),
        "by_status": dict(by_status)
    }

@router.delete("/tasks/{task_id}", status_code=204)
def admin_delete_task(
    task_id: int,
    admin=Depends(require_admin),
    storage=Depends(get_storage)
):
    if not storage.get_by_id(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    storage.delete(task_id)