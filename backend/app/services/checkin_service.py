from backend.app.db.database import SessionLocal
from backend.app.repositories.checkin_repository import CheckinRepository
from backend.app.repositories.subscription_repository import SubscriptionRepository
from backend.app.repositories.enrollment_repository import EnrollmentRepository
from backend.app import exceptions

def create_checkin(member_id: int, class_id: int = None):
    with SessionLocal() as session:
        checkin_repo = CheckinRepository(session)
        sub_repo = SubscriptionRepository(session)
        enroll_repo = EnrollmentRepository(session)

        # 1. Validate Active Subscription
        sub = sub_repo.get_active_by_user(member_id)
        if not sub:
            raise exceptions.BusinessLogicError("No active subscription found")
        
        if sub.status == "frozen":
            raise exceptions.BusinessLogicError("Subscription is frozen")

        # 2. Validate Debt
        if sub.debt > 0:
            raise exceptions.BusinessLogicError(f"Cannot check-in: Member has outstanding debt of {sub.debt}")

        # 3. Validate Remaining Entries
        if sub.remaining_entries is not None:
            if sub.remaining_entries <= 0:
                raise exceptions.BusinessLogicError("No remaining entries left")
            sub_repo.update(sub.id, remaining_entries=sub.remaining_entries - 1)

        # 4. Validate Class Enrollment (if applicable)
        if class_id:
            enrollments = enroll_repo.get_active_by_class(class_id)
            is_enrolled = any(e.member_id == member_id for e in enrollments)
            if not is_enrolled:
                raise exceptions.BusinessLogicError("Member is not actively enrolled in this class session")

        # 5. Create Check-in
        return checkin_repo.create(
            member_id=member_id,
            subscription_id=sub.id,
            class_id=class_id
        )

def get_checkin_by_id(checkin_id: int):
    with SessionLocal() as session:
        return CheckinRepository(session).get_by_id(checkin_id)

def get_checkins_by_member(member_id: int):
    with SessionLocal() as session:
        repo = CheckinRepository(session)
        return session.query(repo.model).filter(repo.model.member_id == member_id).all()

def get_all_checkins():
    with SessionLocal() as session:
        return CheckinRepository(session).get_all()

