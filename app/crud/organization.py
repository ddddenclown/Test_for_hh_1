from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional, List

from app.models import Organization, OrganizationPhone, ActivityType, Building
from app.models.organization import organization_activity
from app.schemas.organization import OrganizationCreate


async def create_organization(
        db: AsyncSession,
        organization_in: OrganizationCreate
) -> Organization:
    building = await db.get(Building, organization_in.building_id)
    if not building:
        raise ValueError("Здание не найдено")

    stmt = select(ActivityType).where(ActivityType.id.in_(organization_in.activity_ids))
    result = await db.execute(stmt)
    activities = result.scalars().all()

    if len(activities) != len(organization_in.activity_ids):
        found_ids = {a.id for a in activities}
        missing_ids = set(organization_in.activity_ids) - found_ids
        raise ValueError(f"Виды деятельности не найдены: {missing_ids}")

    organization = Organization(
        name=organization_in.name,
        building_id=organization_in.building_id,
        activities=activities
    )

    for phone in organization_in.phones:
        organization.phones.append(OrganizationPhone(phone=phone.phone))

    db.add(organization)
    await db.commit()
    await db.refresh(organization)

    await db.refresh(organization, ["building", "activities", "phones"])
    for phone in organization.phones:
        await db.refresh(phone)

    return organization


async def get_organization_by_building(
        db: AsyncSession,
        building_id: int,
) -> List[Organization]:
    building = await db.get(Building, building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здание не найдено"
        )

    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
            selectinload(Organization.phones)
        )
        .where(Organization.building_id == building_id)
    )
    return result.scalars().all()

async def get_organization(
        db: AsyncSession,
        organization_id: int
) -> Optional[Organization]:
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
            selectinload(Organization.phones)
        )
        .where(Organization.id == organization_id)
    )
    return result.scalars().first()


async def search_by_name(
        org_name: str,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 100,
) -> List[Organization]:
    result = await db.execute(
        select(Organization)
        .options(
            selectinload(Organization.building),
            selectinload(Organization.activities),
            selectinload(Organization.phones)
        )
        .where(Organization.name.ilike(f"%{org_name}%"))
        .offset(offset)
        .limit(limit)
        .order_by(Organization.name)
    )
    return result.scalars().all()


async def get_organizations_by_activity_simple(
        db: AsyncSession,
        activity_id: int,
        include_descedant: bool = False,
        offset: int = 0,
        limit: int = 100
) ->List[Organization]:
    result = await db.execute(select(ActivityType))
    all_activities: List[ActivityType] = result.scalars().all()

    children_map: dict[int, List[int]] = {}
    for act in all_activities:
        if act.parent_id is not None:
            children_map.setdefault(act.parent_id, []).append(act.id)

    ids = {activity_id}
    if include_descedant:
        stack = [activity_id]
        while stack:
            current = stack.pop()
            for child_id in children_map.get(current, []):
                if child_id not in ids:
                    ids.add(child_id)
                    stack.append(child_id)

    q = (
        select(Organization)
        .join(organization_activity, Organization.id == organization_activity.c.organization_id)
        .where(organization_activity.c.activity_type_id.in_(ids))
        .options(
            selectinload(Organization.phones),
            selectinload(Organization.activities).selectinload(ActivityType.children)
        )
        .distinct()
        .offset(offset)
        .limit(limit)
        .order_by(Organization.name)
    )
    orgs = (await db.execute(q)).scalars().all()
    return orgs
