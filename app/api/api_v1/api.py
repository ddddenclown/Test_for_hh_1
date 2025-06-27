from fastapi import APIRouter
from app.api.api_v1.routers import building, activity, organization

router = APIRouter()
router.include_router(building.router, prefix="/buildings", tags=["buildings"])
router.include_router(activity.router, prefix="/activities", tags=["activities"])
router.include_router(organization.router, prefix="/organizations", tags=["organizations"])