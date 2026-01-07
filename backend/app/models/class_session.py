from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from backend.app.db.database import Base

class ClassSession(Base):
    __tablename__ = "class_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)  # ← לא nullable
    capacity = Column(Integer, nullable=False)
    trainer_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(
        Enum(
            "scheduled",
            "open",
            "full",
            "closed",
            "canceled",
            name="class_status",
        ),
        nullable=False,
        server_default="scheduled",
    )


    is_registration_closed = Column(Boolean, nullable=False, server_default="0")

    enrollments = relationship("Enrollment", back_populates="class_session")
