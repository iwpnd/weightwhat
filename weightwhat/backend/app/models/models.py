from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class WeightSchema(BaseModel):
    weight: float = Field(..., title="Input weight")
    created_at: datetime = datetime.now()


class WeightDB(WeightSchema):
    id: int = Field(..., title="Primary key of weight")
    created_at: datetime = Field(..., title="Created at %m/%d/%Y, %H:%M:%S")
    updated_at: datetime = None


class WeightFromTo(BaseModel):
    fromdate: datetime
    todate: datetime

    @validator("todate", pre=True, always=True)
    def set_date_now(cls, v):
        if isinstance(v, date):
            return datetime(year=v.year, month=v.month, day=v.day)
        else:
            return datetime.now()

    @validator("fromdate", pre=True, always=True)
    def set_date_past(cls, v):
        if isinstance(v, date):
            return datetime(year=v.year, month=v.month, day=v.day)
        else:
            return datetime(1900, 1, 1)
