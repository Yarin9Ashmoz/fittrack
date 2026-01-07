from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, text
from sqlalchemy.orm import relationship
from backend.app.db.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)
    status = Column(String(20), nullable=False)
    waitlist_position = Column(Integer, nullable=True)

    class_session = relationship("ClassSession", back_populates="enrollments")
