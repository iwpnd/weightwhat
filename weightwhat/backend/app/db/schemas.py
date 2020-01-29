from typing import Tuple

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func

metadata = MetaData()


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
            onupdate=func.now(),
        ),
    )


weights = Table(
    "weights",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("weight", Float, nullable=False),
    *timestamps()
)
