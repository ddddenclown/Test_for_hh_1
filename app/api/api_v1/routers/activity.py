from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.schemas.activity import ActivityCreate, ActivityRead
from app.crud.crud_activity import crud_activity
from app.db.db import get_async_session

router = APIRouter()


@router.post("/", response_model=ActivityRead)
async def create_activity(
        activity_in: ActivityCreate,
        db: AsyncSession = Depends(get_async_session),
):
    return await crud_activity.create(db=db, obj_in=activity_in)


@router.get("/", response_model=ActivityRead)
async def get_activity_type(
        activity_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    activity = await crud_activity.get(db=db,
                                       activity_id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вид деятельности не найден"
        )
    return activity


@router.get("/", response_model=List[ActivityRead])
async def get_all_activity_types(
        level: Optional[int] = Query(None, ge=1, le=3,description="Уровень влооженности от 1 до 3"),
        parent_id: Optional[int]= Query(None, description="Фильтр по родительскому айди"),
        db: AsyncSession = Depends(get_async_session),
):
    return await crud_activity.get_multi(db=db,
                                         level=level,
                                         parent_id=parent_id)