from backend.app.db.database import engine
from backend.app.models.workout_plan import workout_plans
from backend.app.models.workout_item import workout_items
from backend.app.models.user import users
from backend.app.exceptions import NotFoundError, ValidationError
from sqlalchemy import select, insert, update, delete


def create_workout_plan(data):
    with engine.connect() as conn:

        member_query = select(users).where(users.c.id == data.member_id)
        member = conn.execute(member_query).fetchone()
        if not member:
            raise NotFoundError("Member not found")
        if member.role != "member":
            raise ValidationError("User is not a member")

        trainer_query = select(users).where(users.c.id == data.trainer_id)
        trainer = conn.execute(trainer_query).fetchone()
        if not trainer:
            raise NotFoundError("Trainer not found")
        if trainer.role != "trainer":
            raise ValidationError("User is not a trainer")

        insert_query = insert(workout_plans).values(**data.dict())
        result = conn.execute(insert_query)
        plan_id = result.lastrowid

        return get_workout_plan_by_id(plan_id)


def get_workout_plan_by_id(plan_id):
    with engine.connect() as conn:
        query = select(workout_plans).where(workout_plans.c.id == plan_id)
        plan = conn.execute(query).fetchone()

        if not plan:
            raise NotFoundError("Workout plan not found")

        return plan


def get_workout_plans_by_member(member_id):
    with engine.connect() as conn:

        member_query = select(users).where(users.c.id == member_id)
        member = conn.execute(member_query).fetchone()
        if not member:
            raise NotFoundError("Member not found")

        query = select(workout_plans).where(workout_plans.c.member_id == member_id)
        return conn.execute(query).fetchall()



def get_all_workout_plans():
    with engine.connect() as conn:
        return conn.execute(select(workout_plans)).fetchall()


def update_workout_plan(plan_id, data):
    with engine.connect() as conn:

        existing = get_workout_plan_by_id(plan_id)

        update_data = {k: v for k, v in data.dict().items() if v is not None}

        if "trainer_id" in update_data:
            trainer_query = select(users).where(users.c.id == update_data["trainer_id"])
            trainer = conn.execute(trainer_query).fetchone()
            if not trainer:
                raise NotFoundError("Trainer not found")
            if trainer.role != "trainer":
                raise ValidationError("User is not a trainer")

        update_query = (
            update(workout_plans)
            .where(workout_plans.c.id == plan_id)
            .values(**update_data)
        )
        conn.execute(update_query)

        return get_workout_plan_by_id(plan_id)


def delete_workout_plan(plan_id):
    with engine.connect() as conn:

        get_workout_plan_by_id(plan_id)

        delete_query = delete(workout_plans).where(workout_plans.c.id == plan_id)
        conn.execute(delete_query)

        return {"message": "Workout plan deleted"}


def get_exercises_by_plan(plan_id):
    with engine.connect() as conn:

        get_workout_plan_by_id(plan_id)

        query = select(workout_items).where(workout_items.c.plan_id == plan_id)
        return conn.execute(query).fetchall()
