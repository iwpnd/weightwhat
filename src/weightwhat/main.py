from fastapi import FastAPI
from weightwhat.api.api_v1.api import router as api_router
from weightwhat.core.config import PROJECT_NAME, API_V1_STR


app = FastAPI(title=PROJECT_NAME)
app.include_router(api_router, prefix=API_V1_STR)
