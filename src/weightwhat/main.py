from fastapi import FastAPI
from weightwhat.api.api_v1.api import router as api_router
from weightwhat.core.config import PROJECT_NAME, DEBUG, API_PREFIX, VERSION
from weightwhat.db.db import database, engine
from weightwhat.db.schemas import weights, metadata

metadata.create_all(engine)


app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


app.include_router(api_router, prefix=API_PREFIX)
