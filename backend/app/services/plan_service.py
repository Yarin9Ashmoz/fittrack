from backend.app.db.database import engine
from backend.app.models.plan import plans
from backend.app.exceptions import NotFoundError, ValidationError
from sqlalchemy import select, insert, update, delete


def create_plan(data):
    with engine.connect() as conn:

        if data.type == "entries" and data.max_entries is None:
            raise ValidationError("max_entries is required for entry-based plans")

        if data.type == "days" and data.valid_days is None:
            raise ValidationError("valid_days is required for day-based plans")

        insert_query = insert(plans).values(**data.dict())
        result = conn.execute(insert_query)
        plan_id = result.lastrowid

        return get_plan_by_id(plan_id)


def get_plan_by_id(plan_id):
    with engine.connect() as conn:
        query = select(plans).where(plans.c.id == plan_id)
        plan = conn.execute(query).fetchone()

        if not plan:
            raise NotFoundError("Plan not found")

        return plan


def get_all_plans():
    with engine.connect() as conn:
        query = select(plans)
        return conn.execute(query).fetchall()


def update_plan(plan_id, data):
    with engine.connect() as conn:

        existing = get_plan_by_id(plan_id)

        update_data = {k: v for k, v in data.dict().items() if v is not None}

        if "type" in update_data:
            if update_data["type"] == "entries" and update_data.get("max_entries") is None:
                raise ValidationError("max_entries is required for entry-based plans")

            if update_data["type"] == "days" and update_data.get("valid_days") is None:
                raise ValidationError("valid_days is required for day-based plans")

        update_query = (
            update(plans)
            .where(plans.c.id == plan_id)
            .values(**update_data)
        )
        conn.execute(update_query)

        return get_plan_by_id(plan_id)


def delete_plan(plan_id):
    with engine.connect() as conn:

        get_plan_by_id(plan_id)

        delete_query = delete(plans).where(plans.c.id == plan_id)
        conn.execute(delete_query)

        return {"message": "Plan deleted"}
