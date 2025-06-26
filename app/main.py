from fastapi import FastAPI

from app.api.api_v1.api import router
from app.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router, prefix=settings.API_V1_STR)