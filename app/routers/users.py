from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user, get_storage
from app.schemas import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}")
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    storage=Depends(get_storage)
):
    # В реальном приложении здесь был бы запрос к БД пользователей
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return {"id": user_id, "role": current_user.role}