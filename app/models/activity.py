from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.db.db import Base


class ActivityType(Base):
    __tablename__ = "activity_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("activity_types.id", ondelete="CASCADE"), nullable=True)
    level = Column(Integer, nullable=False, default=1)

    __table_args__ = (
        CheckConstraint("level BETWEEN 1 AND 3", name="ck_activity_level_range"),
    )

    parent = relationship(
        "ActivityType",
        remote_side=[id],
        back_populates="children",
        lazy="selectin"
    )

    children = relationship(
        "ActivityType",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities",
        lazy="selectin"
    )