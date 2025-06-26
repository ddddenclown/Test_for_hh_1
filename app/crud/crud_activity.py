from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.activity import ActivityType
from app.schemas.activity import ActivityCreate


class CRUDActivityType:
    async def create(self,
                     db: AsyncSession,
                     *,
                     obj_in: ActivityCreate
                     ) -> ActivityType:
        db_obj = ActivityType(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self,
                  db: AsyncSession,
                  activity_id: int
                  ) -> Optional[ActivityType]:
        result = await db.execute(
            select(ActivityType).where(ActivityType.id == activity_id)
        )
        return result.scalars().first()

    async def get_multi(self,
                        db: AsyncSession,
                        *,
                        max_level: int = 3,
                        offset: int = 0,
                        limit: int = 100
                        ) -> List[ActivityType]:
        result = await db.execute(
            select(ActivityType)
            .where(ActivityType.level <= max_level)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_descendant_ids(self, db: AsyncSession, activity_id: int) -> List[int]:
        result = [activity_id]

        async def fetch_children(parent_ids: List[int]):
            stmt = select(ActivityType.id).where(ActivityType.parent_id.in_(parent_ids))
            res = await db.execute(stmt)
            return res.scalars().all()

        level_1 = await fetch_children([activity_id])
        result.extend(level_1)

        if level_1:
            level_2 = await fetch_children(level_1)
            result.extend(level_2)

            if level_2:
                level_3 = await fetch_children(level_2)
                result.extend(level_3)

        return result


crud_activity = CRUDActivityType()
