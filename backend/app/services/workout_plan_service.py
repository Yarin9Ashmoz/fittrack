from backend.app.db.database import SessionLocal
from backend.app.repositories.workout_plan_repository import WorkoutPlanRepository
from backend.app.repositories.workout_item_repository import WorkoutItemRepository
from backend.app import exceptions

def create_workout_plan(data):
    with SessionLocal() as session:
        return WorkoutPlanRepository(session).create(**data.dict())

def get_workout_plan_by_id(plan_id: int):
    with SessionLocal() as session:
        plan = WorkoutPlanRepository(session).get_by_id(plan_id)
        if not plan:
            raise exceptions.NotFoundError("Workout plan not found")
        return plan

def get_workout_plans_by_member(member_id: int):
    with SessionLocal() as session:
        return WorkoutPlanRepository(session).get_by_member(member_id)

def get_all_workout_plans():
    with SessionLocal() as session:
        return WorkoutPlanRepository(session).get_all()

def update_workout_plan(plan_id, data):
    with SessionLocal() as session:
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        updated = WorkoutPlanRepository(session).update(plan_id, **update_data)
        if not updated:
            raise exceptions.NotFoundError("Workout plan not found")
        return updated

def delete_workout_plan(plan_id):
    with SessionLocal() as session:
        if not WorkoutPlanRepository(session).delete(plan_id):
            raise exceptions.NotFoundError("Workout plan not found")
        return True

def get_exercises_by_plan(plan_id):
    with SessionLocal() as session:
        return WorkoutItemRepository(session).get_by_plan(plan_id)
