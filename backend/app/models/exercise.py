from sqlalchemy import Column, Integer, String
from backend.app.db.database import Base

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True)
