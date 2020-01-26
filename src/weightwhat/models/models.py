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


@dataclass
class WeightFromTo(BaseModel):
    fromdate: Optional[date] = date(1900, 1, 1)
    todate: Optional[date] = date.today()

    @validator("fromdate", pre=True, always=True, whole=True)
    def parse_date_fromdate(cls, fromdate):
        if not fromdate:
            return date.today()
        elif isinstance(fromdate, str):
            return datetime.strptime(fromdate, "%Y%m%d").date()
        else:
            fromdate

    @validator("todate", pre=True, always=True, whole=True)
    def parse_date_todate(cls, todate):
        if not todate:
            return date.today()
        elif isinstance(todate, str):
            return datetime.strptime(todate, "%Y%m%d").date()
        else:
            todate
