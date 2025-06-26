from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from app.models.activity import ActivityType
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate


class CRUDOrganization:
    async def create(self,
                     db: AsyncSession,
                     *,
                     obj_in: OrganizationCreate
                     ) -> Organization:
        db_obj = Organization(
            name=obj_in.name,
            phone_numbers=obj_in.phones,
            building_id = obj_in.building_id,
        )
        db.add(db_obj)
        await db.flush()

        if obj_in.activity_ids:
            activities = await db.execute(
                select(ActivityType).where(ActivityType.id.in_(obj_in.activity_ids))
            )
            db_obj.activities.extend(activities.scalars().all())

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self,
                  db: AsyncSession,
                  organization_id: int
                  ) -> Optional[Organization]:
        result = await db.execute(
            select(Organization)
            .options(selectinload(Organization.building), selectinload(Organization.activities))
            .where(Organization.id == organization_id)
        )
        return result.scalars().first()

    async def get_by_building(self,
                              db: AsyncSession,
                              building_id: int,
                              offset: int = 0,
                              limit: int = 100,
                              ) -> List[Organization]:
        result = await db.execute(
            select(Organization)
            .where(Organization.building_id == building_id)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_name(self,
                          db: AsyncSession,
                          name: str,
                          offset: int = 0,
                          limit: int = 100,
                          ) -> List[Organization]:
        result = await db.execute(
            select(Organization)
            .where(func.lower(Organization.name).ilike(f"%{name.lower()}%"))
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_activity(self,
                              db: AsyncSession,
                              activity_id: int,
                              offset: int = 0,
                              limit: int = 100
                              ) -> List[Organization]:
        result = await db.execute(
            select(Organization)
            .join(Organization.activities)
            .where(ActivityType.id == activity_id)
            .offset(offset)
            .limit(limit)
        )
        return result.scalrs().all()

    async def get_by_activity_with_children(self,
                                            db: AsyncSession,
                                            activity_ids: List[int],
                                            offset: int = 0,
                                            limit: int = 100
                                            ) -> List[Organization]:
        result = await db.execute(
            select(Organization)
            .options(selectinload(Organization.building), selectinload(Organization.activities))
            .join(Organization.activities)
            .filter(ActivityType.id.in_(activity_ids))
            .offset(offset)
            .limit(limit)
            .distinct()
        )
        return result.scalars().all()



crud_organization = CRUDOrganization()