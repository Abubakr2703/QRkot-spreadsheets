from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_project_exists,
                                check_project_has_no_investments)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.user import User
from app.schemas.charity_project import (ProjectCharityCreate,
                                         ProjectCharityDB,
                                         ProjectCharityUpdate)
from app.services.charity_project import (create_project_service,
                                          update_project_service)

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    "/", response_model=list[ProjectCharityDB],
    response_model_exclude_none=True
)
async def get_all_projects(session: SessionDep):
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post("/", response_model=ProjectCharityDB,
             response_model_exclude_none=True)
async def create_project(
    obj_in: ProjectCharityCreate,
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)],
):
    return await create_project_service(obj_in, session)


@router.patch(
    "/{project_id}", response_model=ProjectCharityDB,
    response_model_exclude_none=True
)
async def update_project(
    project_id: int,
    obj_in: ProjectCharityUpdate,
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)],
):
    return await update_project_service(project_id, obj_in, session)


@router.delete(
    "/{project_id}", response_model=ProjectCharityDB,
    response_model_exclude_none=True
)
async def delete_project(
    project_id: int,
    session: SessionDep,
    user: Annotated[User, Depends(current_superuser)],
):
    db_project = await check_project_exists(project_id, session)
    check_project_has_no_investments(db_project)
    return await charity_project_crud.remove(db_project, session)
