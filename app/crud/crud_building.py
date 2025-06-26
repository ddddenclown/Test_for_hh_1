from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.building import Building
from app.schemas.building import BuildingCreate


class CRUDBuilding:
    async def create(self,
                     db: AsyncSession,
                     *,
                     obj_in: BuildingCreate
                     ) -> Building:
        db_obj = Building(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self,
                  db: AsyncSession,
                  building_id: int
                  ) -> Optional[Building]:
        result = await db.execute(
            select(Building).where(Building.id == building_id)
        )
        return result.scalars().first()

    async def get_multi(self,
                        db: AsyncSession,
                        *,
                        offset: int = 0,
                        limit: int = 100
                        ) -> List[Building]:
        result = await db.execute(
            select(Building)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()


crud_buildings = CRUDBuilding()
