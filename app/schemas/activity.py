from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ActivityBase(BaseModel):
    name: str = Field(..., example="Молочная продукция")
    parent_id: Optional[int] = Field(None, description="ID родителя")


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    level: int = Field(..., description="Уровень вложеннности от 1 до 3")
    children: List["ActivityRead"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

ActivityRead.update_forward_refs()