from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.schemas.building import BuildingRead, BuildingCreate
from app.crud.building import create_building, get_all_buildings, get_by_id
from app.db.db import get_async_session


router = APIRouter()


@router.post("/", response_model=BuildingRead)
async def create_new_building(
        building_int: BuildingCreate,
        db: AsyncSession = Depends(get_async_session),
):
    return await create_building(db=db,
                                 obj_in=building_int)


@router.get("/{building_id}", response_model=BuildingRead)
async def get_building_by_id(
        building_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    result = await get_by_id(db=db, building_id=building_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return result


@router.get("/", response_model=List[BuildingRead])
async def get_buildings(
        db: AsyncSession = Depends(get_async_session),
        offset: int = 0,
        limit: int = 100,
):
    result = await get_all_buildings(db=db,
                                     offset=offset,
                                     limit=limit)
    return result
