import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.core.yandex_client import YandexDiskClient, get_yandex_client
from app.crud.charity_project import charity_project_crud
from app.models.user import User
from app.services.yandex_api import create_simple_report

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
SuperUserDep = Annotated[User, Depends(current_superuser)]
ClientDep = Annotated[YandexDiskClient, Depends(get_yandex_client)]


logger = logging.getLogger(__name__)


@router.post(
    "/report/",
    response_model=str,
    summary="Создать отчёт по закрытым проектам",
)
async def create_report(
    session: SessionDep,
    user: SuperUserDep,
    client: ClientDep,
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session)
    if not projects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет закрытых проектов для формирования отчёта",
        )

    try:
        public_url = await create_simple_report(projects, client)
    except Exception:
        logger.exception("Ошибка при создании отчёта на Яндекс Диске")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать отчёт. Попробуйте позже.",
        )

    return public_url