from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.app.db.database import Base

class WorkoutItem(Base):
    __tablename__ = "workout_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_id = Column(Integer, ForeignKey("workout_plans.id"), nullable=False)
    exercise_name = Column(String(100), nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    target_weight = Column(Float, nullable=True)
    notes = Column(String(255), nullable=True)
