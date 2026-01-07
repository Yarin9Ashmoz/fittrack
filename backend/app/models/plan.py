from sqlalchemy import Column, Integer, String, Float
from backend.app.db.database import Base

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    valid_days = Column(Integer, nullable=True)
    max_entries = Column(Integer, nullable=True)
