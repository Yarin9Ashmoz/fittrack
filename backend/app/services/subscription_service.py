from backend.app.db.database import SessionLocal
from backend.app.repositories.subscription_repository import SubscriptionRepository
from backend.app.repositories.plan_repository import PlanRepository
from backend.app import exceptions
from datetime import date, timedelta

def create_subscription(subscription_data):
    with SessionLocal() as session:
        sub_repo = SubscriptionRepository(session)
        plan_repo = PlanRepository(session)

        if sub_repo.get_active_by_user(subscription_data.user_id):
            raise exceptions.DuplicateError("User already has an active subscription")

        plan = plan_repo.get_by_id(subscription_data.plan_id)
        if not plan:
            raise exceptions.NotFoundError("Plan not found")

        # Fallback if valid_days is missing on plan
        days = getattr(plan, 'valid_days', 30) or 30
        start_date = date.today()
        end_date = start_date + timedelta(days=days)

        return sub_repo.create(
            user_id=subscription_data.user_id,
            plan_id=subscription_data.plan_id,
            status="active",
            start_date=start_date,
            end_date=end_date,
            remaining_entries=subscription_data.remaining_entries,
            debt=0.0
        )

def get_subscription_by_id(subscription_id: int):
    with SessionLocal() as session:
        sub = SubscriptionRepository(session).get_by_id(subscription_id)
        if not sub:
            raise exceptions.NotFoundError("Subscription not found")
        return sub

def get_active_subscription(user_id: int):
    with SessionLocal() as session:
        return SubscriptionRepository(session).get_active_by_user(user_id)

def get_subscriptions_by_member(member_id: int):
    with SessionLocal() as session:
        return SubscriptionRepository(session).get_by_user(member_id)

def freeze_subscription(subscription_id: int, frozen_until: date):
    with SessionLocal() as session:
        repo = SubscriptionRepository(session)
        sub = repo.get_by_id(subscription_id)
        if not sub: raise exceptions.NotFoundError("Subscription not found")
        if sub.status != "active": raise exceptions.BusinessLogicError("Only active can be frozen")
        
        return repo.update(subscription_id, status="frozen", frozen_until=frozen_until)

def unfreeze_subscription(subscription_id: int):
    with SessionLocal() as session:
        repo = SubscriptionRepository(session)
        sub = repo.get_by_id(subscription_id)
        if not sub: raise exceptions.NotFoundError("Subscription not found")
        if sub.status != "frozen": raise exceptions.BusinessLogicError("Only frozen can be unfrozen")
        
        return repo.update(subscription_id, status="active", frozen_until=None)

def renew_subscription(subscription_id: int):
    with SessionLocal() as session:
        sub_repo = SubscriptionRepository(session)
        plan_repo = PlanRepository(session)
        sub = sub_repo.get_by_id(subscription_id)
        if not sub: raise exceptions.NotFoundError("Subscription not found")
        
        plan = plan_repo.get_by_id(sub.plan_id)
        if not plan: raise exceptions.NotFoundError("Plan not found")

        today = date.today()
        days = getattr(plan, 'valid_days', 30) or 30
        new_end = max(sub.end_date, today) + timedelta(days=days)

        return sub_repo.update(subscription_id, start_date=today, end_date=new_end, status="active", frozen_until=None)

def get_all_subscriptions():
    with SessionLocal() as session:
        return SubscriptionRepository(session).get_all()

def update_remaining_entries(subscription_id: int, remaining_entries: int):

    with SessionLocal() as session:
        if remaining_entries < 0: raise exceptions.ValidationError("Negative entries")
        return SubscriptionRepository(session).update(subscription_id, remaining_entries=remaining_entries)
