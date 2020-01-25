from weightwhat.models.models import WeightSchema
from weightwhat.db.db import database
from weightwhat.db.schemas import weights
from loguru import logger


def _log_query(query: str, query_params: dict = None) -> None:
    logger.debug(f"query: {str(query)}, values: {query_params}")


async def post(payload: WeightSchema):
    query = weights.insert().values(weight=payload.weight)
    _log_query(query=str(query), query_params=query.parameters)
    return await database.execute(query)


async def get(id: int):
    query = weights.select().where(id == weights.c.id)
    _log_query(query=str(query).replace("\n", ""), query_params=id)
    return await database.fetch_one(query=query)


async def get_all():
    query = weights.select()
    _log_query(query=str(query).replace("\n", ""), query_params="")
    return await database.fetch_all(query=query)
