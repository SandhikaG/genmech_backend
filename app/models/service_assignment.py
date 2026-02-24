from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class ServiceAssignment(Base):
    __tablename__ = "service_assignments"

    id = Column(Integer, primary_key=True, index=True)

    engineer_user_id = Column(Integer, ForeignKey("users.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    service_name = Column(String)
    status = Column(String, default="pending")