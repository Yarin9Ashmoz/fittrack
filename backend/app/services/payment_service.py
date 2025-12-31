from backend.app.db.database import engine
from backend.app.models.payment import payments
from backend.app.models.subscription import subscriptions
from backend.app import exceptions
from sqlalchemy import select, update


def create_payment(data: dict):
    subscription_id = data["subscription_id"]

    with engine.connect() as conn:

        sub = conn.execute(
            select(subscriptions).where(subscriptions.c.id == subscription_id)
        ).fetchone()

        if not sub:
            raise exceptions.NotFoundError("Subscription not found")

        result = conn.execute(payments.insert().values(**data))
        new_id = result.lastrowid

        return get_payment_by_id(new_id)


def get_payment_by_id(payment_id: int):
    with engine.connect() as conn:
        row = conn.execute(
            select(payments).where(payments.c.id == payment_id)
        ).fetchone()

        if not row:
            raise exceptions.NotFoundError("Payment not found")

        return row


def get_payment_by_member(member_id: int):
    with engine.connect() as conn:
        query = (
            select(payments)
            .select_from(payments.join(subscriptions))
            .where(subscriptions.c.user_id == member_id)
        )
        return conn.execute(query).fetchall()


def get_all_payments():
    with engine.connect() as conn:
        return conn.execute(select(payments)).fetchall()



def cancel_payment(payment_id: int):
    with engine.connect() as conn:
        get_payment_by_id(payment_id)

        conn.execute(
            update(payments)
            .where(payments.c.id == payment_id)
            .values(status="canceled")
        )

        return get_payment_by_id(payment_id)
