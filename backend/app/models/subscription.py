from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.sql import func
from backend.app.db.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    status = Column(String(20), nullable=False, default="active")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    remaining_entries = Column(Integer, nullable=True)
    frozen_until = Column(Date, nullable=True)
    debt = Column(Float, nullable=False, default=0.0)
    created_at = Column(Date, server_default=func.now())
