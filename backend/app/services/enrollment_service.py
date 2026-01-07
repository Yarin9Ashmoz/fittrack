from datetime import datetime, timedelta
from backend.app.db.database import SessionLocal
from backend.app.repositories.enrollment_repository import EnrollmentRepository
from backend.app.repositories.class_session_repository import ClassSessionRepository
from backend.app import exceptions

PROMOTION_DEADLINE_HOURS = 2


def create_enrollment(data: dict):
    with SessionLocal() as session:
        enroll_repo = EnrollmentRepository(session)
        class_repo = ClassSessionRepository(session)

        member_id = data["member_id"]
        class_id = data["class_id"]

        cls = class_repo.get_by_id(class_id)
        if not cls:
            raise exceptions.NotFoundError("Class not found")

        # מניעת הרשמה כפולה
        existing = enroll_repo.session.query(enroll_repo.model).filter_by(
            member_id=member_id,
            class_id=class_id
        ).first()
        if existing:
            raise exceptions.BadRequestError("Member already enrolled or waitlisted")

        enrolled_count = enroll_repo.count_enrolled(class_id)

        # יש מקום → נרשם
        if enrolled_count < cls.capacity:
            new_enrollment = enroll_repo.create(
                member_id=member_id,
                class_id=class_id,
                status="enrolled",
                waitlist_position=None
            )
            return new_enrollment

        # אין מקום → תור המתנה
        waitlist_count = enroll_repo.count_waitlist(class_id)

        new_enrollment = enroll_repo.create(
            member_id=member_id,
            class_id=class_id,
            status="waitlist",
            waitlist_position=waitlist_count + 1
        )
        return new_enrollment


def cancel_enrollment(enrollment_id: int):
    with SessionLocal() as session:
        enroll_repo = EnrollmentRepository(session)
        class_repo = ClassSessionRepository(session)

        enrollment = enroll_repo.get_by_id(enrollment_id)
        if not enrollment:
            raise exceptions.NotFoundError("Enrollment not found")

        class_id = enrollment.class_id
        was_enrolled = enrollment.status == "enrolled"

        # ביטול
        enroll_repo.update(
            enrollment_id,
            status="canceled",
            waitlist_position=None
        )

        # אם היה רשום → צריך לקדם מישהו מהתור
        if was_enrolled:
            next_in_line = enroll_repo.get_next_in_waitlist(class_id)

            if next_in_line:
                enroll_repo.update(
                    next_in_line.id,
                    status="promoted",
                    waitlist_position=None,
                    promoted_at=datetime.utcnow(),
                    deadline_at=datetime.utcnow() + timedelta(hours=PROMOTION_DEADLINE_HOURS)
                )

                # רה־אינדוקס של התור
                remaining = enroll_repo.get_waitlist(class_id)
                for i, enr in enumerate(remaining):
                    enroll_repo.update(enr.id, waitlist_position=i + 1)

        return enrollment


def confirm_promotion(enrollment_id: int):
    """המתאמן מאשר את הקידום שלו"""
    with SessionLocal() as session:
        enroll_repo = EnrollmentRepository(session)

        enrollment = enroll_repo.get_by_id(enrollment_id)
        if not enrollment:
            raise exceptions.NotFoundError("Enrollment not found")

        if enrollment.status != "promoted":
            raise exceptions.BadRequestError("Enrollment is not promoted")

        # אישור → הופך ל־enrolled
        enroll_repo.update(
            enrollment_id,
            status="enrolled",
            promoted_at=None,
            deadline_at=None
        )

        return enrollment


def expire_promotions():
    """מנקה קידומים שפג תוקפם"""
    with SessionLocal() as session:
        enroll_repo = EnrollmentRepository(session)

        now = datetime.utcnow()

        expired = enroll_repo.session.query(enroll_repo.model).filter(
            enroll_repo.model.status == "promoted",
            enroll_repo.model.deadline_at < now
        ).all()

        for enr in expired:
            # מחזיר לתור
            enr.status = "waitlist"
            enr.promoted_at = None
            enr.deadline_at = None

        session.commit()

        return expired


def get_enrollments_by_class(class_id: int):
    with SessionLocal() as session:
        return EnrollmentRepository(session).get_by_class(class_id)


def get_enrollments_by_member(member_id: int):
    with SessionLocal() as session:
        return EnrollmentRepository(session).get_by_member(member_id)


def get_all_enrollments():
    with SessionLocal() as session:
        return EnrollmentRepository(session).get_all()
