from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

# Аутентификация и регистрация
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@router.delete("/users/{id}")
async def delete_user_disabled(id: int):
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено"
    )

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)
