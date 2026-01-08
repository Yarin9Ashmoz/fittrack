from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, text
from sqlalchemy.orm import relationship
from backend.app.db.database import Base
from datetime import datetime

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)
    status = Column(String(20), nullable=False)  # 'active', 'waitlist', 'cancelled'
    waitlist_position = Column(Integer, nullable=True)
    
    # Waitlist management fields
    enrolled_at = Column(DateTime, nullable=True)
    waitlist_joined_at = Column(DateTime, nullable=True)
    promotion_attempted_at = Column(DateTime, nullable=True)
    promotion_method = Column(String(20), nullable=True)  # 'auto', 'manual'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    class_session = relationship("ClassSession", back_populates="enrollments")
