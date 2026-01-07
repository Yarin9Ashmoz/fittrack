from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from backend.app.db.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    paid_at = Column(DateTime, server_default=func.now())
    reference = Column(String(100), nullable=True)
