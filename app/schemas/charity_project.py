from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

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

    @model_validator(mode='before')
    @classmethod
    def reject_explicit_null(cls, data):
        """Запрещает явно передавать null в PATCH-запросе.

        Поле можно не передавать - тогда оно не изменится.
        Но если поле передано со значением null - это ошибка.
        """
        if isinstance(data, dict):
            for field in ('name', 'description', 'full_amount'):
                if field in data and data[field] is None:
                    raise ValueError(
                        f'Поле "{field}" не может быть null'
                    )
        return data


class ProjectCharityDB(ProjectCharityCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
