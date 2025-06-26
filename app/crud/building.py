from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from fastapi import HTTPException, status

from app.schemas.building import BuildingCreate, BuildingRead
from app.models.building import Building


async def create_building(db: AsyncSession,
                          obj_in: BuildingCreate,
                          ) -> BuildingRead:
    is_building = await db.execute(
        select(Building)
        .where(Building.address == obj_in.address)
    )
    if is_building.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Building already exists"
        )
    building = Building(
        address=obj_in.address,
        latitude=obj_in.latitude,
        longitude=obj_in.longitude,
    )
    db.add(building)
    await db.commit()
    await db.refresh(building)
    return building


async def get_by_id(db: AsyncSession,
                    building_id: int
                    ) -> Optional[BuildingRead]:
    result = await db.execute(
        select(Building)
        .where(Building.id == building_id)
    )
    return result.scalars().first()


async def get_all_buildings(db: AsyncSession,
                            offset: int = 0,
                            limit: int = 100,
                            ) -> List[BuildingRead]:
    result = await db.execute(
        select(Building)
        .offset(offset)
        .limit(limit)
    )
    return result.scalars().all()