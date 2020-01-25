from pydantic import BaseModel, Field
from datetime import datetime


class WeightSchema(BaseModel):
    weight: float = Field(..., title="Input weight")


class WeightDB(WeightSchema):
    id: int = Field(..., title="Primary key of weight")
    created_at: str = Field(..., title="Created at %m/%d/%Y, %H:%M:%S")
