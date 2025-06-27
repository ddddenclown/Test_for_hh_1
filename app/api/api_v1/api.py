from fastapi import APIRouter
from app.api.api_v1.routers import building, activity, organization

router = APIRouter()
router.include_router(building.router, prefix="/buildings", tags=["building"])
router.include_router(activity.router, prefix="/activities", tags=["activity"])
router.include_router(organization.router, prefix="/organizations", tags=["organization"])