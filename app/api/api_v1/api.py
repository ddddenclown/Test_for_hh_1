from fastapi import APIRouter
from app.api.api_v1.routers import buildings, activity, organization

router = APIRouter()
router.include_router(buildings.router, prefix="/auth", tags=["building"])
router.include_router(activity.router, prefix="/activity", tags=["activity"])
router.include_router(organization.router, prefix="/organization", tags=["organization"])