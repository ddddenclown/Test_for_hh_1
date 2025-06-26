from pydantic import BaseModel, Field, ConfigDict

class BuildingBase(BaseModel):
    address: str = Field(..., example="г. Казань, ул. Баумана, д.10")
    latitude: float = Field(..., ge=-90, le=90, example=12.345)
    longitude: float = Field(..., ge=-180, le=180, example=23.456)


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)