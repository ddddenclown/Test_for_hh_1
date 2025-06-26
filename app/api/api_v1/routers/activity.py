from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.db import get_async_session
from app.schemas.activity import ActivityCreate, ActivityRead
from app.crud.activity import get_activity_type, get_all_activity_types, create_activity_type, get_activity_tree


router = APIRouter()


@router.post("/", response_model=ActivityRead)
async def create_type_activity(
        activiti_in: ActivityCreate,
        db: AsyncSession = Depends(get_async_session),
):
    try:
        return await create_activity_type(db=db, obj_in=activiti_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/tree", response_model=List[ActivityRead])
async def get_activity_tree_endpoint(db: AsyncSession = Depends(get_async_session)):
    return await get_activity_tree(db=db)


@router.get("/{activity_id}", response_model=ActivityRead)
async def get_activity(
        activity_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    activity = await get_activity_type(db=db, activity_id=activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найдено"
        )
    return activity


@router.get("/", response_model=List[ActivityRead])
async def list_activities(db: AsyncSession = Depends(get_async_session)):
    return await get_all_activity_types(db=db)

