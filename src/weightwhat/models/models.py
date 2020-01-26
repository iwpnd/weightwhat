from pydantic import BaseModel, Field
import pydantic
from datetime import datetime, date


class WeightSchema(BaseModel):
    weight: float = Field(..., title="Input weight")
    created_at: datetime = datetime.now()


class WeightDB(WeightSchema):
    id: int = Field(..., title="Primary key of weight")
    created_at: datetime = Field(..., title="Created at %m/%d/%Y, %H:%M:%S")
    updated_at: datetime = None


def parse_date(cls, value) -> date:
    return datetime.strptime(value, "%Y%m%d").date()


def date_validator(field: str) -> classmethod:
    decorator = pydantic.validator(field, pre=True, allow_reuse=True)
    validator = decorator(parse_date)
    return validator


class WeightFromTo(BaseModel):
    fromdate: date = None
    todate: date = None

    # validators
    _ensure_fromdate_is_normalized: classmethod = date_validator("fromdate")
    _ensure_todate_is_normalized: classmethod = date_validator("todate")
