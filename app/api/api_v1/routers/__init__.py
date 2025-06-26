from .activity import router as activity_router
from .building import router as building_router
from .organization import router as organization_router

__all__ = ["activity_router", "building_router", "organization_router"]