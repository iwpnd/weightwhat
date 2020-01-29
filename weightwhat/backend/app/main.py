from app.api.api_v1.api import router as api_router
from app.core.config import API_PREFIX
from app.core.config import DEBUG
from app.core.config import PROJECT_NAME
from app.core.config import VERSION
from app.db.db import database
from app.db.db import engine
from app.db.schemas import metadata
from fastapi import FastAPI

metadata.create_all(engine)


app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


app.include_router(api_router, prefix=API_PREFIX)
