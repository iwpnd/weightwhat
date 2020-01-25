from weightwhat.models.models import WeightSchema
from weightwhat.db.db import database
from weightwhat.db.schemas import weights


async def post(payload: WeightSchema):
    query = weights.insert().values(weight=payload.weight)
    return await database.execute(query)
