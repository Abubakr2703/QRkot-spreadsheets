from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate
from app.services.investment import process_investment


async def create_donation_service(
    obj_in: DonationCreate, session: AsyncSession, user_id: int
):
    new_donation = await donation_crud.create(obj_in, session, user_id=user_id)
    await session.flush()
    await process_investment(new_donation, session)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
