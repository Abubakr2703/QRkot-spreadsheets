from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):

    async def get_not_fully_invested(self, session: AsyncSession):
        result = await session.execute(
            select(self.model)
            .where(self.model.fully_invested.is_(False))
            .order_by(self.model.create_date)
        )
        return result.scalars().all()

    async def get_by_user(self, user_id: int, session: AsyncSession):
        result = await session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.create_date)
        )
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
