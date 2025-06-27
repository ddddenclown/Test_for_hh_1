from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.building import BuildingRead
from app.schemas.activity import ActivityRead


class OrganizationPhone(BaseModel):
    phone: str = Field(..., example="8-800-555-35-35")

    model_config = ConfigDict(from_attributes=True)


class OrganizationBase(BaseModel):
    name: str = Field(..., example="ООО 'Рога и Копыта")
    building_id: Optional[int] = Field(None, description="Id здагия")
    activity_ids: List[int] = Field(..., description="Список ID видов деятельности", example=[1,2,3])
    phones: List[OrganizationPhone] = Field(default_factory=list, description="Список телефонов")


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationRead(BaseModel):
    id: int
    name: str
    building: Optional[BuildingRead] = None
    activities: List[ActivityRead] = Field(default_factory=list)
    phones: List[OrganizationPhone] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)