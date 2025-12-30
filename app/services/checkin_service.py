from app.db.database import engine
from app.models.checkin import checkins
from app import exceptions
from datetime import datetime
from app.services.subscription_service import (
    get_active_subscription,
    update_remaining_entries
)

def create_checkin(member_id: int, class_id: int):
    with engine.connect() as conn:
        sub = get_active_subscription(member_id)
        if not sub:
            raise exceptions.BusinessLogicError("No active subscription found for member")
        if sub.status == "frozen":
            raise exceptions.BusinessLogicError("Subscription is frozen")
        if sub.remaining_entries is not None:
            if sub.remaining_entries <= 0:
                raise exceptions.BusinessLogicError("No remaining entries left")
            update_remaining_entries(sub.id, sub.remaining_entries -1)

        insert_query = checkins.insert().values(
            member_id=member_id,
            subscription_id=sub.id,
            class_id=class_id
        )
        result = conn.execute(insert_query)
        checkin_id = result.lastrowid
        return get_checkin_by_id(checkin_id)

def get_checkin_by_id(checkin_id: int):
    with engine.connect() as conn:
        query = checkins.select().where(checkins.c.id == checkin_id)
        row = conn.execute(query).fetchone()
        if not row:
            raise exceptions.NotFoundError("Check-in not found")
        return row

def get_checkins_by_member(member_id: int):
    with engine.connect() as conn:
        query = checkins.select().where(checkins.c.member_id == member_id)
        return conn.execute(query).fetchall()

