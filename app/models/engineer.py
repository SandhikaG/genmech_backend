from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base# ✅ IMPORTANT
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Engineer(Base):
    __tablename__ = "engineers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    address = Column(String)
    portfolio_image = Column(String)
    services_completed = Column(Integer, default=0)

    user = relationship("User", back_populates="engineer_profile")