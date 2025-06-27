from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.db import get_async_session
from app.schemas.organization import OrganizationCreate, OrganizationRead
from app.crud.organization import create_organization, get_organization, get_organization_by_building, search_by_name, \
    get_organizations_by_activity_simple, get_organizations_in_radius, get_organizations_in_rectangle, get_all_organizations

router = APIRouter()

@router.post("/", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_new_organization(
    organization_in: OrganizationCreate,
    db: AsyncSession = Depends(get_async_session),
):
    try:
        organization = await create_organization(db, organization_in)
        return organization
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/organizations", response_model=List[OrganizationRead])
async def list_all_organizations(
        db: AsyncSession = Depends(get_async_session),
        offset: int = 0,
        limit: int = 100,
):
    return await get_all_organizations(db=db,
                                       offset=offset,
                                       limit=limit
                                       )


@router.get("/building/{building_id}", response_model=List[OrganizationRead])
async def get_organization_in_building(
        building_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    result = await get_organization_by_building(db=db, building_id=building_id)
    return result


@router.get("/search/{name}", response_model=List[OrganizationRead])
async def search_organizations_by_name(
        org_name: str,
        db: AsyncSession = Depends(get_async_session),
):
    return await search_by_name(db=db, org_name=org_name)


@router.get(
    "/by-activity/{activity_id}",
    response_model=List[OrganizationRead],
    summary="Организации по виду деятельности"
)
async def list_by_activity_simple(
    activity_id: int,
    include_descendants: bool = Query(False, description="Включить потомков"),
    db: AsyncSession = Depends(get_async_session),
        offset: int = 0,
        limit: int = 100
):
    orgs = await get_organizations_by_activity_simple(db=db,
                                                      activity_id=activity_id,
                                                      include_descedant=include_descendants,
                                                      offset=offset,
                                                      limit=limit)
    if not orgs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организации по этому виду деятельности не найдены"
        )
    return orgs


@router.get("/nearby", response_model=List[OrganizationRead], summary="Организации в радиусе")
async def get_organizations_nearby(
    lat: float = Query(..., description="Широта центра"),
    lon: float = Query(..., description="Долгота центра"),
    radius_km: float = Query(..., description="Радиус в км"),
    db: AsyncSession = Depends(get_async_session)
):
    orgs = await get_organizations_in_radius(db, lat, lon, radius_km)
    if not orgs:
        raise HTTPException(status_code=404, detail="Организации в радиусе не найдены")
    return orgs


@router.get("/in-rectangle", response_model=List[OrganizationRead], summary="Организации в прямоугольной области")
async def get_organizations_in_area(
    lat_min: float = Query(..., description="Минимальная широта"),
    lat_max: float = Query(..., description="Максимальная широта"),
    lon_min: float = Query(..., description="Минимальная долгота"),
    lon_max: float = Query(..., description="Максимальная долгота"),
    db: AsyncSession = Depends(get_async_session)
):
    orgs = await get_organizations_in_rectangle(db, lat_min, lat_max, lon_min, lon_max)
    if not orgs:
        raise HTTPException(status_code=404, detail="Организации в области не найдены")
    return orgs


@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization_by_id(
        organization_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    result = await get_organization(db=db, organization_id=organization_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нету!!"
        )
    return result
