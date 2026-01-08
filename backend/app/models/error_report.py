from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from backend.app.db.database import Base

class ErrorReport(Base):
    """
    System error tracking and monitoring for admin oversight.
    Captures exceptions, errors, and system issues.
    """
    __tablename__ = "error_reports"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    error_type = Column(String(100), nullable=False)  # Exception type
    error_message = Column(Text, nullable=False)
    stack_trace = Column(Text, nullable=True)
    
    occurred_at = Column(DateTime, nullable=False, server_default=func.now())
    url = Column(String(500), nullable=True)  # Request path where error occurred
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # User who encountered it
    
    severity = Column(
        Enum("low", "medium", "high", "critical", name="error_severity"),
        nullable=False,
        server_default="medium"
    )
    
    status = Column(
        Enum("new", "investigating", "resolved", "ignored", name="error_status"),
        nullable=False,
        server_default="new"
    )
    
    resolved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)  # Admin notes on resolution
