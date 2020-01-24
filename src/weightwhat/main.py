from fastapi import FastAPI
from weightwhat.api.api_v1.api import router as api_router
from weightwhat.core.config import PROJECT_NAME, DEBUG, API_PREFIX, VERSION


app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
app.include_router(api_router, prefix=API_PREFIX)
