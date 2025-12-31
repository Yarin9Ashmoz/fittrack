from backend.app.db.database import engine
from backend.app.models.enrollment import enrollments
from backend.app.models.class_session import class_sessions
from backend.app import exceptions
from sqlalchemy import select, update, delete


def create_enrollment(data: dict):
    member_id = data["member_id"]
    class_id = data["class_id"]

    with engine.connect() as conn:

        class_row = conn.execute(
            select(class_sessions).where(class_sessions.c.id == class_id)
        ).fetchone()

        if not class_row:
            raise exceptions.NotFoundError("Class not found")

        existing = conn.execute(
            select(enrollments).where(
                enrollments.c.member_id == member_id,
                enrollments.c.class_id == class_id,
                enrollments.c.status == "active"
            )
        ).fetchone()

        if existing:
            raise exceptions.BusinessLogicError("Member is already enrolled in this class")

        current_count = conn.execute(
            select(enrollments).where(
                enrollments.c.class_id == class_id,
                enrollments.c.status == "active"
            )
        ).fetchall()

        if len(current_count) >= class_row.capacity:
            raise exceptions.BusinessLogicError("Class is full")

        result = conn.execute(enrollments.insert().values(**data))
        new_id = result.lastrowid

        return get_enrollment_by_id(new_id)


def get_enrollment_by_id(enrollment_id: int):
    with engine.connect() as conn:
        row = conn.execute(
            select(enrollments).where(enrollments.c.id == enrollment_id)
        ).fetchone()

        if not row:
            raise exceptions.NotFoundError("Enrollment not found")

        return row


def get_enrollments_by_class(class_id: int):
    with engine.connect() as conn:
        return conn.execute(
            select(enrollments).where(enrollments.c.class_id == class_id)
        ).fetchall()


def get_enrollments_by_member(member_id: int):
    with engine.connect() as conn:
        return conn.execute(
            select(enrollments).where(enrollments.c.member_id == member_id)
        ).fetchall()


def get_all_enrollments():
    with engine.connect() as conn:
        return conn.execute(select(enrollments)).fetchall()


def cancel_enrollment(enrollment_id: int):
    with engine.connect() as conn:
        get_enrollment_by_id(enrollment_id)

        conn.execute(
            update(enrollments)
            .where(enrollments.c.id == enrollment_id)
            .values(status="canceled")
        )

        return get_enrollment_by_id(enrollment_id)
