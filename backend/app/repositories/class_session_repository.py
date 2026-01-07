from .base_repository import BaseRepository
from ..models.class_session import ClassSession
from ..models.enrollment import Enrollment
from sqlalchemy import func

class ClassSessionRepository(BaseRepository[ClassSession]):
    def __init__(self, session):
        super().__init__(ClassSession, session)
        self.session = session

    # 1. ספירת משתתפים רשומים
    def count_enrolled(self, session_id: int):
        return (
            self.session.query(func.count(Enrollment.id))
            .filter(
                Enrollment.class_id == session_id,
                Enrollment.status == "enrolled"
            )
            .scalar()
        )

    # 2. ספירת תור המתנה
    def count_waitlist(self, session_id: int):
        return (
            self.session.query(func.count(Enrollment.id))
            .filter(
                Enrollment.class_id == session_id,
                Enrollment.status == "waitlist"
            )
            .scalar()
        )

    # 3. שליפת כל ההרשמות לשיעור
    def get_enrollments(self, session_id: int):
        return (
            self.session.query(Enrollment)
            .filter(Enrollment.class_id == session_id)
            .all()
        )

    # 4. שליפת תור לפי סדר
    def get_waitlist_ordered(self, session_id: int):
        return (
            self.session.query(Enrollment)
            .filter(
                Enrollment.class_id == session_id,
                Enrollment.status == "waitlist"
            )
            .order_by(Enrollment.waitlist_position.asc())
            .all()
        )

    # 5. עדכון סטטוס שיעור
    def update_status(self, session_id: int, new_status: str):
        cls = self.get_by_id(session_id)
        if not cls:
            return None
        cls.status = new_status
        self.session.commit()
        return cls

    # 6. בדיקה אם השיעור מלא
    def is_full(self, session_id: int):
        cls = self.get_by_id(session_id)
        enrolled = self.count_enrolled(session_id)
        return enrolled >= cls.capacity
