from weightwhat.api.api_v1 import crud
from weightwhat.models.models import WeightDB, WeightSchema
from fastapi import APIRouter, HTTPException
from datetime import datetime
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from loguru import logger

router = APIRouter()


@router.post("/weight", response_model=WeightDB, status_code=HTTP_201_CREATED)
async def create_weight(payload: WeightSchema) -> WeightDB:
    """
    INSERT a weight

    This will insert a weight into the database.

    And this path operation will:

    Example:
    * return {
        "id": primary_key,
        "weight: 88.1,
        "created_at": "2020-11-01 13:37:00"
    }
    """

    weight_id = await crud.post(payload)
    response_object = {
        "id": weight_id,
        "weight": payload.weight,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return response_object
