from flask import Blueprint, jsonify, request
from backend.app.schemas.workout_item import (
    WorkoutItemCreateSchema,
    WorkoutItemUpdateSchema,
    WorkoutItemResponseSchema,
)
from backend.app.services.workout_item_service import (
    create_workout_item,
    get_items_by_plan,
    get_workout_item_by_id,
    update_workout_item,
    delete_workout_item,
    get_all_workout_items,
)


workout_items_bp = Blueprint("workout_items", __name__, url_prefix="/workout-items")

@workout_items_bp.get('/')
def get_all_workout_items_route():
    items = get_all_workout_items()
    return jsonify([WorkoutItemResponseSchema.from_orm(i).dict() for i in items]), 200

@workout_items_bp.post('/')
def create_workout_item_route():
    data = request.get_json()
    workout_item_data = WorkoutItemCreateSchema(**data)
    new_workout_item = create_workout_item(workout_item_data)
    return jsonify(WorkoutItemResponseSchema.from_orm(new_workout_item).dict()), 201

@workout_items_bp.get('/plan/<int:plan_id>')
def get_items_by_plan_route(plan_id):
    items = get_items_by_plan(plan_id)
    return jsonify([WorkoutItemResponseSchema.from_orm(i).dict() for i in items]), 200

@workout_items_bp.get('/<int:item_id>')
def get_workout_item_by_id_route(item_id):
    item = get_workout_item_by_id(item_id)
    return jsonify(WorkoutItemResponseSchema.from_orm(item).dict()), 200

@workout_items_bp.put('/<int:item_id>')
def update_workout_item_route(item_id):
    data = request.get_json()
    workout_item_data = WorkoutItemUpdateSchema(**data)
    updated = update_workout_item(item_id,workout_item_data)
    return jsonify(WorkoutItemResponseSchema.from_orm(updated).dict()), 200

@workout_items_bp.delete('/<int:item_id>')
def delete_workout_item_route(item_id):
    delete_workout_item(item_id)
    return jsonify({"message": "Workout item deleted"}), 200