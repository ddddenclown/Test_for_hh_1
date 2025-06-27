from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader

from app.api.api_v1.api import router
from app.core.config import settings


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неверный API key"
        )


app = FastAPI(title=settings.PROJECT_NAME, dependencies=[Depends(verify_api_key)])

app.include_router(router, prefix=settings.API_V1_STR)