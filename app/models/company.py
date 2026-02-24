from sqlalchemy import Column, String,Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
import uuid
from app.db.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    company_email = Column(String, nullable=False)
    company_phone = Column(String)
    company_address = Column(String)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())