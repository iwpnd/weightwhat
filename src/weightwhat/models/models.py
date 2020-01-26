from pydantic import BaseModel, Field, validator
from pydantic.dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


class WeightSchema(BaseModel):
    weight: float = Field(..., title="Input weight")
    created_at: datetime = datetime.now()


class WeightDB(WeightSchema):
    id: int = Field(..., title="Primary key of weight")
    created_at: datetime = Field(..., title="Created at %m/%d/%Y, %H:%M:%S")
    updated_at: datetime = None


class WeightFromTo(BaseModel):
    fromdate: date = None
    todate: date = None

    @validator("todate", pre=True, always=True)
    def set_date_now(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%Y%m%d").date()
        else:
            return date.today()

    @validator("fromdate", pre=True, always=True)
    def set_date_past(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%Y%m%d").date()
        else:
            return date(1900, 1, 1)
