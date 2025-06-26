from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from sqlalchemy.orm import selectinload

from app.models.activity import ActivityType
from app.schemas.activity import ActivityCreate, ActivityRead


async def create_activity_type(db: AsyncSession,
                               obj_in: ActivityCreate
                               ) -> ActivityType:
    activity = ActivityType(name=obj_in.name)

    if obj_in.parent_id:
        result = await db.execute(
            select(ActivityType)
            .filter_by(id=obj_in.parent_id)
        )
        parent = result.scalar_one_or_none()
        if not parent:
            raise ValueError("Родитель не найден")
        activity.parent = parent

    db.add(activity)
    await db.commit()
    await db.refresh(activity)
    return activity


async def get_activity_type(db: AsyncSession,
                            activity_id: int,
                            ):
    result = await db.execute(
        select(ActivityType)
        .options(
            selectinload(ActivityType.children).selectinload(ActivityType.children)
        )
        .where(ActivityType.id == activity_id)
    )
    return result.scalars().first()


async def get_all_activity_types(db: AsyncSession):
    result = await db.execute(
        select(ActivityType).options(selectinload(ActivityType.children))
    )
    return result.scalars().all()


async def get_activity_tree(db: AsyncSession) -> List[ActivityRead]:
    result = await db.execute(
        select(ActivityType)
        .options(
            selectinload(ActivityType.children)
            .selectinload(ActivityType.children)
            .selectinload(ActivityType.children)
        )
        .filter(ActivityType.parent_id == None)
    )
    root_nodes = result.scalars().all()

    def to_dto(node: ActivityType) -> ActivityRead:
        return ActivityRead(
            id=node.id,
            name=node.name,
            parent_id=node.parent_id,
            level=node.level,
            children=[to_dto(child) for child in node.children]
        )
    return [to_dto(node) for node in root_nodes]