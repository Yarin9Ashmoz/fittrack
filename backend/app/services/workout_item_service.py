from backend.app.db.database import SessionLocal
from backend.app.repositories.workout_item_repository import WorkoutItemRepository
from backend.app.repositories.workout_plan_repository import WorkoutPlanRepository
from backend.app import exceptions

def create_workout_item(data):
    with SessionLocal() as session:
        plan = WorkoutPlanRepository(session).get_by_id(data.plan_id)
        if not plan:
            raise exceptions.NotFoundError("Workout plan not found")
        return WorkoutItemRepository(session).create(**data.dict())

def get_workout_item_by_id(item_id):
    with SessionLocal() as session:
        item = WorkoutItemRepository(session).get_by_id(item_id)
        if not item:
            raise exceptions.NotFoundError("Workout item not found")
        return item

def get_all_workout_items():
    with SessionLocal() as session:
        return WorkoutItemRepository(session).get_all()

def update_workout_item(item_id, data):
    with SessionLocal() as session:
        update_data = {k: v for k, v in data.dict().items() if v is not None}
        updated = WorkoutItemRepository(session).update(item_id, **update_data)
        if not updated:
            raise exceptions.NotFoundError("item not found")
        return updated

def delete_workout_item(item_id):
    with SessionLocal() as session:
        if not WorkoutItemRepository(session).delete(item_id):
            raise exceptions.NotFoundError("item not found")
        return True

def get_items_by_plan(plan_id: int):
    with SessionLocal() as session:
        return WorkoutItemRepository(session).get_by_plan(plan_id)

