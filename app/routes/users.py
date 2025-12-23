from flask import Blueprint, request, jsonify
from app.schemas.user import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from app.services.user_service import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)

users_bp = Blueprint("users", __name__)

@users_bp.post("/")
def create_user_route():
    data = request.json
    user_data = UserCreateSchema(**data)
    new_user = create_user(user_data)
    return jsonify(UserResponseSchema.from_orm(new_user).dict()), 201

@users_bp.get("/")
def get_all_users_route():
    users = get_all_users()
    return jsonify([UserResponseSchema.from_orm(u).dict() for u in users]), 200

@users_bp.get("/<int:user_id>")
def get_user_route(user_id):
    user = get_user_by_id(user_id)
    return jsonify(UserResponseSchema.from_orm(user).dict()), 200

@users_bp.put("/<int:user_id>")
def update_user_route(user_id):
    data = request.json
    user_data = UserUpdateSchema(**data)
    updated = update_user(user_id, user_data)
    return jsonify(UserResponseSchema.from_orm(updated).dict()), 200

@users_bp.delete("/<int:user_id>")
def delete_user_route(user_id):
    delete_user(user_id)
    return jsonify({"message": "User deleted"}), 200
