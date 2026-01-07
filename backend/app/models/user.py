from sqlalchemy import Column, Integer, String
from backend.app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    national_id = Column(String(20), nullable=True, unique=True)
    password_hash = Column(String(255), nullable=True) # Will be mandatory after auth fix
    address = Column(String(255))
    role = Column(String(20), nullable=False) # admin, trainer, member
    status = Column(String(20), nullable=False, default="active")
