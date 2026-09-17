from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_open_projects(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        """
        Возвращает все проекты, которые ещё не полностью профинансированы,
        отсортированные по дате создания (первые созданные — первыми).
        Используется для распределения нового пожертвования.
        """
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return result.scalars().all()

    async def get_projects_by_completion_rate(self, session: AsyncSession):
        """Возвращает список закрытых проектов,
        отсортированных по времени сбора."""
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(True))
            .order_by(
                (self.model.close_date - self.model.create_date).asc()
            )
        )
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
