from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Проверяет, существует ли проект, и возвращает его."""
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="Проект не найден")
    return project


async def check_project_name_duplicate(
    name: str, session: AsyncSession, exclude_id: Optional[int] = None
) -> None:
    stmt = select(CharityProject).where(CharityProject.name == name)
    if exclude_id is not None:
        stmt = stmt.where(CharityProject.id != exclude_id)
    result = await session.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует",
        )


def check_project_not_closed(project: CharityProject) -> None:
    """Проверяет, что проект не закрыт."""
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Закрытый проект нельзя редактировать",
        )


def check_new_amount_more_than_invested(
    project: CharityProject, new_full_amount: int
) -> None:
    """Проверяет, что новая требуемая сумма не меньше уже инвестированной."""
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Новую сумму нельзя установить ниже уже инвестированной",
        )


def check_project_has_no_investments(project: CharityProject) -> None:
    """Проверяет, что в проект ещё не инвестировали."""
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Нельзя удалить проект,"
            "где уже были инвестированы средства",
        )
