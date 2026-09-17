from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (DonationCreate, DonationCreateResponse,
                                  DonationOut)
from app.services.donation import create_donation_service

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/my", response_model=list[DonationCreateResponse],
    response_model_exclude_none=True
)
async def get_my_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    """Получить список пожертвований текущего пользователя."""
    donations = await donation_crud.get_by_user(user.id, session)
    return donations


@router.get("/", response_model=list[DonationOut],
            response_model_exclude_none=True)
async def get_all_donations(
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)],
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.post(
    "/", response_model=DonationCreateResponse,
    response_model_exclude_none=True
)
async def create_donation(
    obj_in: DonationCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_user)],
):
    return await create_donation_service(obj_in, session, user.id)
