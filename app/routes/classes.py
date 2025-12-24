from flask import Blueprint, request, jsonify
from app.schemas.class_session import (
    ClassCreateSchema,
    ClassUpdateSchema,
    ClassResponseSchema
)
from app.services.class_service import (
    create_class,
    get_all_classes,
    get_class_by_id,
    update_class,
    delete_class
)

classes_bp = Blueprint("classes", __name__)

@classes_bp.post("/")
def create_class_route():
    data = request.json
    class_data = ClassCreateSchema(**data)
    new_class = create_class(class_data)
    return jsonify(ClassResponseSchema.from_orm(new_class).dict()), 201

@classes_bp.get("/")
def get_all_classes_route():
    classes = get_all_classes()
    return jsonify([ClassResponseSchema.from_orm(c).dict() for c in classes]), 200

@classes_bp.get("/<int:class_id>")
def get_class_by_id_route(class_id):
    c = get_class_by_id(class_id)
    return jsonify(ClassResponseSchema.from_orm(c).dict()), 200

@classes_bp.put("/<int:class_id>")
def update_class_route(class_id):
    data = request.json
    class_data = ClassUpdateSchema(**data)
    updated = update_class(class_id, class_data)
    return jsonify(ClassResponseSchema.from_orm(updated).dict()), 200

@classes_bp.delete("/<int:class_id>")
def delete_class_route(class_id):
    delete_class(class_id)
    return jsonify({"message":"Class deleted"}), 200

