from datetime import date
from datetime import datetime
from typing import List

from app.api.api_v1 import crud
from app.models.models import WeightDB
from app.models.models import WeightFromTo
from app.models.models import WeightSchema
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path
from loguru import logger
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_404_NOT_FOUND

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
    logger.debug(f"received: {payload.weight} / {payload.created_at}")
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
async def get_weight(id: int = Path(..., gt=0)):
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


@router.get("/weight", response_model=WeightDB, status_code=HTTP_200_OK)
async def get_latest_weight() -> WeightDB:
    """
    Get latest weight by created_at

    This will fetch the latest created date.

    And this path operation will:

    * return {
        "id": primary_key,
        "weight: 88.1,
        "created_at": "2020-11-01 13:37:00",
        "updated_at": "2020-11-01 13:37:00"
    }
    """

    weight = await crud.get_latest()

    if not weight:
        raise HTTPException(HTTP_404_NOT_FOUND, detail="no weights found")

    return weight


@router.get("/weights", response_model=List[WeightDB], status_code=HTTP_200_OK)
async def get_all_weights(fromdate: date = None, todate: date = None) -> WeightDB:
    """
    Get all weights

    This will fetch all weights that are currently stored in the database without exceptions

    Optionally:
    **fromdate**: date %Y-%m-%s defaults to: 1900-01-01
    **todate**: date %Y-%m-%s defaults to: date.today()

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

    # if at least one date is given the other defaults to either the beginning (date(1900,1,1)) or
    # date.today(). If no date is given at all, all records will be returned
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


@router.put("/weight/{id}", response_model=WeightDB)
async def update_weight(payload: WeightSchema, id: int = Path(..., gt=0)) -> WeightDB:
    """
    Update a weight with :id

    This will let you update an existing weight in the database. You can update :weight and :created_at,
    or just the :weight, but weight should always be present during an update.

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
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="weight not found")

    update_data = payload.dict(exclude_unset=True)

    # returns one record object that is subscriptable
    weight_record = await crud.put(id, update_data)

    weight_id = weight_record[0][0]
    weight_updated_at = weight_record[0][1]
    weight_created_at = weight_record[0][2]
    weight_weight = weight_record[0][3]

    response_object = {
        "id": weight_id,
        "weight": weight_weight,
        "created_at": weight_created_at,
        "updated_at": weight_updated_at,
    }

    return response_object


@router.delete("/weight/{id}")
async def delete_weight(id: int = Path(..., gt=0)) -> WeightDB:
    """
    Delete a weight with :id

    This will delete a weight by :id from the database

    And this path operation will:

    Return the entry that has successfully been deleted.

    * return {
        "id": primary_key,
        "weight: 88.1,
        "created_at": "2020-11-01 13:37:00",
        "updated_at": "2020-11-01 13:37:00"
    }
    """
    weight = await crud.get(id)
    if not weight:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="weight not found")

    await crud.delete(id)

    return weight
