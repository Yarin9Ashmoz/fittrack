from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum, Numeric
from sqlalchemy.sql import func
from backend.app.db.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)  # Made nullable
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Track which member
    
    # Payment method tracking
    payment_method = Column(
        Enum("closed_lesson", "subscription", "manual", name="payment_method_type"),
        nullable=False,
        server_default="manual"
    )
    
    class_session_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=True)  # If for specific class
    
    # Amount calculation
    calculated_amount = Column(Numeric(10, 2), nullable=False)  # Auto-calculated amount
    discount_applied = Column(Numeric(10, 2), nullable=False, default=0)
    amount = Column(Float, nullable=False)  # Final amount (calculated - discount) - keep for backward compatibility
    
    status = Column(String(20), nullable=False, default="pending")
    paid_at = Column(DateTime, nullable=True)  # Changed to nullable, set when actually paid
    reference = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())

