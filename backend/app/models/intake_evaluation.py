from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.db.database import Base

class IntakeEvaluation(Base):
    """
    Psychological and physical intake evaluation for new members.
    Records mental status, cognitive function, and physical limitations.
    """
    __tablename__ = "intake_evaluations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    evaluation_date = Column(DateTime, nullable=False, server_default=func.now())
    
    # JSON fields for flexible structured data
    mental_status = Column(JSON, nullable=True)  # mood, anxiety, stress levels
    cognitive_function = Column(JSON, nullable=True)  # memory, focus, decision-making scores
    physical_limitations = Column(JSON, nullable=True)  # injuries, restrictions, medical conditions
    
    cleared_for_training = Column(Boolean, nullable=False, default=False)
    notes = Column(Text, nullable=True)
    evaluated_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
