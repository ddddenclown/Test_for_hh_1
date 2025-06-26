from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.building import BuildingCreate, BuildingRead
from app.crud.crud_building import crud_buildings
from app.db.db import get_async_session

router = APIRouter()


@router.post("/", response_model=BuildingRead)
async def create_building(
        building_in: BuildingCreate,
        db: AsyncSession = Depends(get_async_session),
):
    return await crud_buildings.create(db=db,obj_in=building_in)


@router.get("/{building_id}", response_model=BuildingRead)
async def get_building(
        building_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    building = await crud_buildings.get(db=db, building_id=building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здание не найдено"
        )
    return building


@router.get("/", response_model=List[BuildingRead])
async def get_all_buildings(
        offset: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_async_session),
):
    return await crud_buildings.get_multi(db=db, offset=offset, limit=limit)