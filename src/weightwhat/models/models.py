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
