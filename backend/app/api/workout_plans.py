from flask import Blueprint, jsonify, request
from backend.app.schemas.workout_plan import (
    WorkoutPlanCreateSchema,
    WorkoutPlanUpdateSchema,
    WorkoutPlanResponseSchema,
)
from backend.app.services.workout_plan_service import (
    create_workout_plan,
    get_workout_plans_by_member,
    get_workout_plan_by_id,
    update_workout_plan,
    delete_workout_plan,
    get_exercises_by_plan,
    get_all_workout_plans
)
from backend.app.exceptions import NotFoundError, ValidationError


workout_plans_bp = Blueprint("workout_plans", __name__, url_prefix="/workout-plans")


@workout_plans_bp.get("/")
def get_all_workout_plans_route():
    plans = get_all_workout_plans()
    # Using generic dict conversion if schema fails or based on other patterns, but lets attempt schema list
    return jsonify([WorkoutPlanResponseSchema.from_orm(p).dict() for p in plans]), 200

@workout_plans_bp.post("/")
def create_workout_plan_route():
    try:
        data = request.get_json()
        workout_plan_data = WorkoutPlanCreateSchema(**data)
        new_workout_plan = create_workout_plan(workout_plan_data)
        return jsonify(WorkoutPlanResponseSchema.from_orm(new_workout_plan).dict()), 201

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@workout_plans_bp.get("/member/<int:member_id>")
def get_workout_by_member_route(member_id):
    try:
        workout_plans = get_workout_plans_by_member(member_id)
        return jsonify([WorkoutPlanResponseSchema.from_orm(w).dict() for w in workout_plans]), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@workout_plans_bp.get("/<int:plan_id>")
def get_workout_by_plan_route(plan_id):
    try:
        workout_plan = get_workout_plan_by_id(plan_id)
        return jsonify(WorkoutPlanResponseSchema.from_orm(workout_plan).dict()), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@workout_plans_bp.put("/<int:plan_id>")
def update_workout_plan_route(plan_id):
    try:
        data = request.get_json()
        workout_plan_data = WorkoutPlanUpdateSchema(**data)
        updated = update_workout_plan(plan_id, workout_plan_data)
        return jsonify(WorkoutPlanResponseSchema.from_orm(updated).dict()), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@workout_plans_bp.delete("/<int:plan_id>")
def delete_workout_plan_route(plan_id):
    try:
        delete_workout_plan(plan_id)
        return jsonify({"message": "Workout plan deleted"}), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404


@workout_plans_bp.get("/<int:plan_id>/exercises")
def get_exercises_by_plan_route(plan_id):
    try:
        exercises = get_exercises_by_plan(plan_id)
        return jsonify([dict(e) for e in exercises]), 200

    except NotFoundError as e:
        return jsonify({"error": str(e)}), 404
