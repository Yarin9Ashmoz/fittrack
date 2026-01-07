from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.app.db.database import Base

class Checkin(Base):
    __tablename__ = "checkins"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())
