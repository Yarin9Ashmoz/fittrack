from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from backend.app.db.database import Base

class PersonalTracking(Base):
    """
    Ongoing personal tracking for members covering emotional, cognitive,
    social, and physical metrics over time.
    """
    __tablename__ = "personal_tracking"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tracking_date = Column(DateTime, nullable=False, server_default=func.now())
    
    # JSON fields for flexible tracking data
    emotional_regulation = Column(JSON, nullable=True)  # mood, stress, coping mechanisms
    symptom_tracking = Column(JSON, nullable=True)  # physical/mental symptoms
    social_function = Column(JSON, nullable=True)  # social interactions, support network
    physical_function = Column(JSON, nullable=True)  # energy, sleep, pain, mobility
    
    notes = Column(Text, nullable=True)
    recorded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # member or trainer
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
