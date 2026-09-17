from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def process_investment(target, session: AsyncSession):
    """
    Распределяет средства из подходящих источников в целевую сущность.
    Если target – проект, то источники – пожертвования с остатком.
    Если target – пожертвование, то источники – открытые проекты.
    Изменения НЕ коммитятся — вызывающий обязан сделать commit.
    """
    if target.invested_amount >= target.full_amount:
        target.fully_invested = True
        target.close_date = datetime.now()
        return target

    if isinstance(target, CharityProject):
        sources = await donation_crud.get_not_fully_invested(session)
    elif isinstance(target, Donation):
        sources = await charity_project_crud.get_open_projects(session)
    else:
        raise TypeError("target должен быть CharityProject или Donation")

    for source in sources:
        if target.invested_amount >= target.full_amount:
            break

        available = source.full_amount - source.invested_amount
        needed = target.full_amount - target.invested_amount
        amount = min(available, needed)
        if amount <= 0:
            continue

        source.invested_amount += amount
        target.invested_amount += amount

        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = datetime.now()

        if target.invested_amount == target.full_amount:
            target.fully_invested = True
            target.close_date = datetime.now()
            break

    return target
