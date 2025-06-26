from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.db import Base


organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_type_id", Integer, ForeignKey("activity_types.id", ondelete="CASCADE"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="SET NULL"), nullable=True)

    building = relationship(
        "Building",
        back_populates="organizations",
        lazy="joined",
    )

    activities = relationship(
        "ActivityType",
        secondary=organization_activity,
        back_populates="organizations",
        lazy="selectin",
    )

    phones = relationship(
        "OrganizationPhone",
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )



class OrganizationPhone(Base):
    __tablename__ = "organization_phones"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    phone = Column(String(50), nullable=False)

    organization = relationship(
        "Organization",
        back_populates="phones",
        lazy="joined",
    )
