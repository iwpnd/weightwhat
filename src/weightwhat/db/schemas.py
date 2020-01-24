from weightwhat.db.db import metadata
from sqlalchemy import Column, DateTime, Integer, Float, Table
from sqlalchemy.sql import func
from typing import Tuple


def timestamps() -> Tuple[Column, Column]:
    return (
        Column(
            "created_at",
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        Column(
            "updated_at",
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
    )


weights = Table(
    "weights",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("weight", Float, nullable=False),
    *timestamps()
)
