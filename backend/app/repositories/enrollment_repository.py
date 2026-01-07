from .base_repository import BaseRepository
from ..models.enrollment import Enrollment
from sqlalchemy import func

class EnrollmentRepository(BaseRepository[Enrollment]):
    def __init__(self, session):
        super().__init__(Enrollment, session)
        self.session = session

    # כל ההרשמות לשיעור
    def get_by_class(self, class_id: int):
        return (
            self.session.query(Enrollment)
            .filter(Enrollment.class_id == class_id)
            .all()
        )

    # משתתפים רשומים (enrolled)
    def get_enrolled(self, class_id: int):
        return (
            self.session.query(Enrollment)
            .filter(
                Enrollment.class_id == class_id,
                Enrollment.status == "enrolled"
            )
            .all()
        )

    # תור המתנה (waitlist)
    def get_waitlist(self, class_id: int):
        return (
            self.session.query(Enrollment)
            .filter(
                Enrollment.class_id == class_id,
                Enrollment.status == "waitlist"
            )
            .order_by(Enrollment.waitlist_position.asc())
            .all()
        )

    # משתמש שקודם מהתור (promoted)
    def get_promoted(self, class_id: int):
        return (
            self.session.query(Enrollment)
            .filter(
                Enrollment.class_id == class_id,
                Enrollment.status == "promoted"
            )
            .all()
        )

    # ספירת משתתפים רשומים
    def count_enrolled(self, class_id: int):
        return (
            self.session.query(func.count(Enrollment.id))
            .filter(
                Enrollment.class_id == class_id,
                Enrollment.status == "enrolled"
            )
            .scalar()
        )

    # ספירת תור המתנה
    def count_waitlist(self, class_id: int):
        return (
            self.session.query(func.count(Enrollment.id))
            .filter(
                Enrollment.class_id == class_id,
                Enrollment.status == "waitlist"
            )
            .scalar()
        )

    # ההרשמות של משתמש מסוים
    def get_by_member(self, member_id: int):
        return (
            self.session.query(Enrollment)
            .filter(Enrollment.member_id == member_id)
            .all()
        )

    # הבא בתור (לצורך קידום)
    def get_next_in_waitlist(self, class_id: int):
        return (
            self.session.query(Enrollment)
            .filter(
                Enrollment.class_id == class_id,
                Enrollment.status == "waitlist"
            )
            .order_by(Enrollment.waitlist_position.asc())
            .first()
        )
