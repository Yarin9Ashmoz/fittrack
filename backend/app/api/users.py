from flask import Blueprint, request, jsonify
from backend.app.schemas.user import UserCreateSchema, UserUpdateSchema, UserResponseSchema
from backend.app.services.user_service import (
    create_user,
    get_user_by_id,
    get_all_users,
    update_user,
    delete_user
)

from backend.app.utils.security import roles_required, token_required

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.post("/")
@token_required
@roles_required('admin')
def create_user_route():
    data = request.get_json()
    user_data = UserCreateSchema(**data)
    new_user = create_user(user_data)
    return jsonify(UserResponseSchema.from_orm(new_user).dict()), 201

@users_bp.get("/")
@token_required
def get_all_users_route():
    users = get_all_users()
    return jsonify([UserResponseSchema.from_orm(u).dict() for u in users]), 200

@users_bp.get("/<int:user_id>")
@token_required
def get_user_route(user_id):
    user = get_user_by_id(user_id)
    return jsonify(UserResponseSchema.from_orm(user).dict()), 200

@users_bp.put("/<int:user_id>")
@token_required
@roles_required('admin')
def update_user_route(user_id):
    data = request.json
    user_data = UserUpdateSchema(**data)
    updated = update_user(user_id, user_data)
    return jsonify(UserResponseSchema.from_orm(updated).dict()), 200

@users_bp.delete("/<int:user_id>")
@token_required
@roles_required('admin')
def delete_user_route(user_id):
    delete_user(user_id)
    return jsonify({"message": "User deleted"}), 200
