from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, text
from backend.app.db.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    status = Column(String(20), nullable=False, server_default=text("'active'")) # active, canceled, waitlisted
    waitlist_position = Column(Integer, nullable=True)
