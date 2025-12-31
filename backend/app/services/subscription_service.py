from backend.app.db.database import engine
from backend.app.models.subscription import subscriptions
from backend.app.models.plan import plans
from backend.app import exceptions
from datetime import date, timedelta


def create_subscription(subscription_data):
    with engine.connect() as conn:

        active = get_active_subscription(subscription_data.user_id)
        if active:
            raise exceptions.DuplicateError("User already has an active subscription")

        plan_query = plans.select().where(plans.c.id == subscription_data.plan_id)
        plan = conn.execute(plan_query).fetchone()

        if not plan:
            raise exceptions.NotFoundError("Plan not found")

        start_date = date.today()
        end_date = start_date + timedelta(days=plan.duration_days)

        insert_query = subscriptions.insert().values(
            user_id=subscription_data.user_id,
            plan_id=subscription_data.plan_id,
            status="active",
            start_date=start_date,
            end_date=end_date,
            remaining_entries=subscription_data.remaining_entries,
            frozen_until=None
        )

        result = conn.execute(insert_query)
        subscription_id = result.lastrowid

        return get_subscription_by_id(subscription_id)


def get_subscription_by_id(subscription_id: int):
    with engine.connect() as conn:
        query = subscriptions.select().where(subscriptions.c.id == subscription_id)
        sub = conn.execute(query).fetchone()

        if not sub:
            raise exceptions.NotFoundError("Subscription not found")

        return sub


def get_active_subscription(user_id: int):
    with engine.connect() as conn:
        query = subscriptions.select().where(
            (subscriptions.c.user_id == user_id) &
            (subscriptions.c.status == "active")
        )
        return conn.execute(query).fetchone()


def get_subscriptions_by_member(member_id: int):
    with engine.connect() as conn:
        query = subscriptions.select().where(subscriptions.c.user_id == member_id)
        return conn.execute(query).fetchall()


def get_all_subscriptions():
    with engine.connect() as conn:
        query = subscriptions.select()
        return conn.execute(query).fetchall()


def freeze_subscription(subscription_id: int, frozen_until: date):
    with engine.connect() as conn:
        sub = get_subscription_by_id(subscription_id)

        if sub.status != "active":
            raise exceptions.BusinessLogicError("Only active subscriptions can be frozen")

        if frozen_until <= date.today():
            raise exceptions.ValidationError("Frozen until date must be in the future")

        update_query = subscriptions.update().where(
            subscriptions.c.id == subscription_id
        ).values(
            status="frozen",
            frozen_until=frozen_until
        )

        conn.execute(update_query)
        return get_subscription_by_id(subscription_id)


def unfreeze_subscription(subscription_id: int):
    with engine.connect() as conn:
        sub = get_subscription_by_id(subscription_id)

        if sub.status != "frozen":
            raise exceptions.BusinessLogicError("Only frozen subscriptions can be unfrozen")

        query = subscriptions.update().where(subscriptions.c.id == subscription_id).values(
            status="active",
            frozen_until=None
        )

        conn.execute(query)
        return get_subscription_by_id(subscription_id)


def renew_subscription(subscription_id: int):
    with engine.connect() as conn:
        sub = get_subscription_by_id(subscription_id)
        plan_query = plans.select().where(plans.c.id == sub.plan_id)
        plan = conn.execute(plan_query).fetchone()

        if not plan:
            raise exceptions.NotFoundError("Plan not found")

        today = date.today()
        if sub.end_date >= today:
            new_end = sub.end_date + timedelta(days=plan.duration_days)
        else:
            new_end = today + timedelta(days=plan.duration_days)

        update_query = subscriptions.update().where(
            subscriptions.c.id == subscription_id
        ).values(
            start_date=today,
            end_date=new_end,
            status="active",
            frozen_until=None
        )
        conn.execute(update_query)
        return get_subscription_by_id(subscription_id)

def update_remaining_entries(subscription_id: int, remaining_entries: int):
    with engine.connect() as conn:
        sub = get_subscription_by_id(subscription_id) # Ensure subscription exists
        if remaining_entries < 0:
            raise exceptions.ValidationError("Remaining entries cannot be negative")
        query = subscriptions.update().where(
            subscriptions.c.id == subscription_id
        ).values(
            remaining_entries=remaining_entries
        )
        conn.execute(query)
        return get_subscription_by_id(subscription_id)


