from weightwhat.api.api_v1 import crud
from weightwhat.models.models import WeightDB, WeightSchema
from fastapi import APIRouter, HTTPException
from datetime import datetime
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

router = APIRouter()


@router.post("/weight", response_model=WeightDB, status_code=HTTP_201_CREATED)
async def create_weight(payload: WeightSchema) -> WeightDB:
    weight_id = await crud.post(payload)

    response_object = {
        "id": weight_id,
        "weight": payload.weight,
        "created_at": datetime.now().strftime("%m/%d/%YT%H:%M:%S"),
    }

    return response_object
