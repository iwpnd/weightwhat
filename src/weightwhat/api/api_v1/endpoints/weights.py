from weightwhat.api.api_v1 import crud
from weightwhat.models.models import WeightDB, WeightSchema, WeightFromTo
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, date
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from loguru import logger
from typing import List

router = APIRouter()


@router.post("/weight", response_model=WeightDB, status_code=HTTP_201_CREATED)
async def create_weight(payload: WeightSchema) -> WeightDB:
    """
    INSERT a weight

    This will insert a weight into the database.

    And this path operation will:

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
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not payload.created_at
        else payload.created_at,
    }

    return response_object


@router.get("/weight/{id}", response_model=WeightDB, status_code=HTTP_200_OK)
async def get_weight(id: int):
    """
    Get a weight by id

    This will fetch a weight with a given id

    And this path operation will:

    * return {
        "id": primary_key,
        "weight: 88.1,
        "created_at": "2020-11-01 13:37:00",
        "updated_at": "2020-11-01 13:37:00"
    }
    """
    weight = await crud.get(id)
    if not weight:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="weight id not found"
        )

    return weight


@router.get("/weights", response_model=List[WeightDB], status_code=HTTP_200_OK)
async def get_all_weights(fromdate: date = None, todate: date = None):
    """
    Get all weights

    This will fetch all weights that are currently stored in the database without exceptions

    And this path operation will:

    * return [
        {
        "id": 1,
        "weight: 88.1,
        "created_at": "2020-11-01 13:37:00",
        "updated_at": "2020-11-01 13:37:00"
        },
        {
        "id": 2,
        "weight: 88.2,
        "created_at": "2020-11-02 13:37:00",
        "updated_at": "2020-11-02 13:37:00"
        },
        ]
    """

    if fromdate or todate:
        limit_dates = WeightFromTo(fromdate=fromdate, todate=todate)
        weights = await crud.get_all(
            fromdate=limit_dates.fromdate, todate=limit_dates.todate
        )
    else:
        weights = await crud.get_all()

    if not weights:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="no weights found")

    return weights
