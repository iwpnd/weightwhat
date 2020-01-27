from weightwhat.models.models import WeightSchema
from weightwhat.db.db import database
from weightwhat.db.schemas import weights
from loguru import logger
from datetime import datetime, date
from weightwhat.core.config import STRFTIME


def _log_query(query: str, query_params: dict = None) -> None:
    logger.debug(f"query: {str(query)}, values: {query_params}")


async def post(payload: WeightSchema):
    query = weights.insert().values(
        weight=payload.weight,
        created_at=datetime.now().strftime(STRFTIME)
        if not payload.created_at
        else payload.created_at,
    )
    _log_query(query=str(query), query_params=query.parameters)
    return await database.execute(query)


async def get(id: int):
    query = weights.select().where(id == weights.c.id)
    _log_query(query=str(query).replace("\n", ""), query_params=id)
    return await database.fetch_one(query=query)


async def get_all(fromdate: datetime = None, todate: datetime = None):
    if fromdate or todate:
        query = (
            weights.select()
            .where(weights.c.created_at <= todate)
            .where(weights.c.created_at >= fromdate)
        )
    else:
        query = weights.select()

    _log_query(query=str(query).replace("\n", ""), query_params="")
    return await database.fetch_all(query=query)


async def put(id: int, payload: WeightSchema):
    logger.debug(f"received: {payload}")
    query = (
        weights.update()
        .where(id == weights.c.id)
        .values(payload)
        .returning(
            weights.c.id, weights.c.updated_at, weights.c.created_at, weights.c.weight
        )
    )

    return await database.fetch_all(query=query)
