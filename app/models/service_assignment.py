from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
import uuid
from app.db.database import Base

class ServiceAssignment(Base):
    __tablename__ = "service_assignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engineer_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    company_name = Column(String, nullable=False)
    service_name = Column(String, nullable=False)

    status = Column(String, default="pending")

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())