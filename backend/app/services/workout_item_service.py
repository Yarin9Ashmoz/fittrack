from backend.app.db.database import engine
from backend.app.models.workout_item import workout_items
from backend.app.models.workout_plan import workout_plans
from backend.app import exceptions
from sqlalchemy import select, insert, update, delete

def create_workout_item(data):
    with engine.connect() as conn:
        plan_query = select(workout_plans).where(workout_plans.c.id == data.plan_id)
        plan = conn.execute(plan_query).fetchone()
        if not plan:
            raise exceptions.NotFoundError("Workout plan not found")

        insert_query = insert(workout_items).values(**data.dict())
        result = conn.execute(insert_query)
        item_id = result.lastrowid
        return get_workout_item_by_id(item_id)

def get_workout_item_by_id(item_id):
    with engine.connect() as conn:
        query = select(workout_items).where(workout_items.c.id == item_id)
        item = conn.execute(query).fetchone()
        if not item:
            raise exceptions.NotFoundError("Workout item not found")
        return item

def get_items_by_plan(plan_id):
    with engine.connect() as conn:
        plan_query = select(workout_plans).where(workout_plans.c.id == plan_id)
        plan = conn.execute(plan_query).fetchone()
        if not plan:
            raise exceptions.NotFoundError("workout plan not found")

        item_query = select(workout_items).where(workout_items.c.plan_id == plan_id)
        return conn.execute(item_query).fetchall()

def update_workout_item(item_id, data):
    with engine.connect() as conn:
        existing = get_workout_item_by_id(item_id)

        update_data = {k: v for k, v in data.dict().items() if v is not None}
        update_query = update(workout_items).where(workout_items.c.id == item_id).values(**update_data)
        conn.execute(update_query)
        return get_workout_item_by_id(item_id)

def delete_workout_item(item_id):
    with engine.connect() as conn:
        get_workout_item_by_id(item_id)

        query = delete(workout_items).where(workout_items.c.id == item_id)
        conn.execute(query)
        return {'message': 'Workout item deleted'}

def get_all_workout_items():
    with engine.connect() as conn:
        query = select(workout_items)
        return conn.execute(query).fetchall()



