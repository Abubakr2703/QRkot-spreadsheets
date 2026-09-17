from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_new_amount_more_than_invested,
                                check_project_exists,
                                check_project_name_duplicate,
                                check_project_not_closed)
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (ProjectCharityCreate,
                                         ProjectCharityUpdate)
from app.services.investment import process_investment


async def create_project_service(
    obj_in: ProjectCharityCreate,
    session: AsyncSession,
):
    """Создаёт проект и выполняет инвестирование в одной транзакции."""
    await check_project_name_duplicate(obj_in.name, session)
    new_project = await charity_project_crud.create(obj_in, session)
    await session.flush()
    await process_investment(new_project, session)
    await session.commit()
    await session.refresh(new_project)
    return new_project


async def update_project_service(
    project_id: int,
    obj_in: ProjectCharityUpdate,
    session: AsyncSession,
):
    """Обновляет проект и выполняет инвестирование в одной транзакции."""
    db_project = await check_project_exists(project_id, session)
    await session.refresh(db_project)
    check_project_not_closed(db_project)
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session,
                                           exclude_id=project_id)
    if obj_in.full_amount is not None:
        check_new_amount_more_than_invested(db_project, obj_in.full_amount)
    db_project = await charity_project_crud.update(db_project, obj_in, session)
    await process_investment(db_project, session)
    await session.commit()
    await session.refresh(db_project)
    return db_project
