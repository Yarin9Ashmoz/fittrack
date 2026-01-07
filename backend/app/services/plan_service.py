from backend.app.db.database import SessionLocal
from backend.app.repositories.plan_repository import PlanRepository
from backend.app import exceptions

def create_plan(plan_data):
    with SessionLocal() as session:
        return PlanRepository(session).create(**plan_data.dict())

def get_plan_by_id(plan_id: int):
    with SessionLocal() as session:
        plan = PlanRepository(session).get_by_id(plan_id)
        if not plan:
            raise exceptions.NotFoundError("Plan not found")
        return plan

def get_all_plans():
    with SessionLocal() as session:
        return PlanRepository(session).get_all()

def update_plan(plan_id: int, plan_data):
    with SessionLocal() as session:
        update_data = {k: v for k, v in plan_data.dict().items() if v is not None}
        updated = PlanRepository(session).update(plan_id, **update_data)
        if not updated:
            raise exceptions.NotFoundError("Plan not found")
        return updated

def delete_plan(plan_id: int):
    with SessionLocal() as session:
        if not PlanRepository(session).delete(plan_id):
            raise exceptions.NotFoundError("Plan not found")
        return True
