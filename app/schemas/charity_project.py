from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

NAME_MIN_LENGTH = 5
NAME_MAX_LENGTH = 100
DESCRIPTION_MIN_LENGTH = 10


class ProjectCharityBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH
    )
    description: Optional[str] = Field(None, min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: Optional[int] = Field(None, gt=0)


class ProjectCharityCreate(ProjectCharityBase):
    name: str = Field(..., min_length=NAME_MIN_LENGTH,
                      max_length=NAME_MAX_LENGTH)
    description: str = Field(..., min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: int = Field(..., gt=0)
    model_config = ConfigDict(extra="forbid")


class ProjectCharityUpdate(ProjectCharityBase):
    model_config = ConfigDict(extra="forbid")


class ProjectCharityDB(ProjectCharityCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
