from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.db import get_async_session
from app.schemas.organization import OrganizationCreate, OrganizationRead
from app.crud.organization import create_organization, get_organization, get_organization_by_building, search_by_name

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


@router.get("/id/{organization_id}", response_model=OrganizationRead)
async def get_organization_by_id(
        org_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    result = await get_organization(db=db, organization_id=org_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нету!!"
        )
    return result


@router.get("/building/{building_id}", response_model=List[OrganizationRead])
async def get_organization_in_building(
        building_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    result = await get_organization_by_building(db=db, building_id=building_id)
    return result


@router.get("/names/{name}", response_model=List[OrganizationRead])
async def search_organizations_by_name(
        org_name: str,
        db: AsyncSession = Depends(get_async_session),
):
    return await search_by_name(db=db, org_name=org_name)