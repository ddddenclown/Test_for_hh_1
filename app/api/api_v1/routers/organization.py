from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud.crud_organization import crud_organization
from app.crud.crud_activity import crud_activity
from app.schemas.organization import OrganizationCreate, OrganizationRead
from app.db.db import get_async_session


router = APIRouter()


@router.post("/", response_model=OrganizationRead)
async def create_organization(
        organization_in: OrganizationCreate,
        db: AsyncSession = Depends(get_async_session),
):
    return await crud_organization.create(db=db,obj_in=organization_in)


@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization(
        organization_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    organization = await crud_organization.get(db=db, organization_id=organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организация не найдена"
        )
    return organization


@router.get("/", response_model=List[OrganizationRead])
async def get_organizations_by_building(
        building_id: int = Query(..., description="ID здания"),
        offset: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_async_session),
):
    return await crud_organization.get_by_building(
        db=db,
        building_id=building_id,
        offset=offset,
        limit=limit,
    )


@router.get("/search/", response_model=List[OrganizationRead])
async def search_organization_by_name(
        name: str = Query(..., description="Название организации"),
        offset: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_async_session),
):
    return await crud_organization.get_by_name(
        db=db,
        name=name,
        offset=offset,
        limit=limit
    )


@router.get("/by-activity/{activity_id}", response_model=List[OrganizationRead])
async def get_organizations_by_activity_with_children(
    activity_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: AsyncSession = Depends(get_async_session)
):
    activity_ids = await crud_activity.get_descendant_ids(db, activity_id)
    if not activity_ids:
        raise HTTPException(status_code=404, detail="Activity not found")

    return await crud_organization.get_by_activity_with_children(
        db, activity_ids=activity_ids, offset=offset, limit=limit
    )