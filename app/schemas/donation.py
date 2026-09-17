from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str] = Field(None)
    model_config = ConfigDict(extra="forbid")


class DonationOut(BaseModel):
    id: int
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None
    comment: Optional[str] = None
    user_id: int
    model_config = ConfigDict(from_attributes=True)


class DonationCreateResponse(BaseModel):
    id: int
    full_amount: int
    create_date: datetime
    comment: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
