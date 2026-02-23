from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base# ✅ IMPORTANT

class Engineer(Base):
    __tablename__ = "engineers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    address = Column(String)
    portfolio_image = Column(String)
    services_completed = Column(Integer, default=0)

    user = relationship("User", back_populates="engineer_profile")