from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.models.Base import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)


    organizations = relationship(
        "Organization",
        back_populates="building",
        cascade="all, delete-orphan",
        lazy="selectin"
    )