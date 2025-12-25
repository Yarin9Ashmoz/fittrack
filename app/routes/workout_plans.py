from flask import Blueprint, jsonify, request
from app.schemas.workout_plan import (
    WorkoutPlanCreateSchema,
    WorkoutPlanUpdateSchema,
    WorkoutPlanResponseSchema,
)
from app.services.workout_plan_service import (
    create_workout_plan,
    get_workout_plans_by_member,
    get_workout_plan_by_id,
    update_workout_plan,
    delete_workout_plan,
    get_exercises_by_plan
)

workout_plans_bp = Blueprint("workout_plans", __name__)

@workout_plans_bp.post("/")
def create_workout_plan_route():
    data = request.get_json()
    workout_plan_data = WorkoutPlanCreateSchema(**data)
    new_workout_plan = create_workout_plan(workout_plan_data)
    return jsonify(WorkoutPlanResponseSchema.from_orm(new_workout_plan).dict()), 201

@workout_plans_bp.get("/member/<int:member_id>")
def get_workout_by_member_route(member_id):
    workout_plans = get_workout_plans_by_member(member_id)
    return jsonify([WorkoutPlanResponseSchema.from_orm(w).dict() for w in workout_plans]), 200

@workout_plans_bp.get("/<int:plan_id>")
def get_workout_by_plan_route(plan_id):
    workout_plan = get_workout_plan_by_id(plan_id)
    return jsonify(WorkoutPlanResponseSchema.from_orm(workout_plan).dict()), 200

@workout_plans_bp.put("/<int:plan_id>")
def update_workout_plan_route(plan_id):
    data = request.get_json()
    workout_plan_data = WorkoutPlanUpdateSchema(**data)
    updated = update_workout_plan(plan_id, workout_plan_data)
    return jsonify(WorkoutPlanResponseSchema.from_orm(updated).dict()), 200

@workout_plans_bp.delete("/<int:plan_id>")
def delete_workout_plan_route(plan_id):
    delete_workout_plan(plan_id)
    return jsonify({"message": "Workout plan deleted"}), 200

@workout_plans_bp.get("/<int:plan_id>/exercises")
def get_exercises_by_plan_route(plan_id):
    exercises = get_exercises_by_plan(plan_id)
    return jsonify(exercises), 200
