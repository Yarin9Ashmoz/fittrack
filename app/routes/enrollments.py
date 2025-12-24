from flask import Blueprint, request, jsonify
from app.schemas.enrollment import (
    EnrollmentCreateSchema, EnrollmentResponseSchema

)
from app.services.enrollment_service import (
    create_enrollment,
    get_enrollments_by_class,
    get_enrollments_by_member,
    cancel_enrollment
)

enrollments_bp = Blueprint("enrollments", __name__)

@enrollments_bp.post("/")
def create_enrollment_route():
    data = request.get_json()
    enrollment_data = EnrollmentCreateSchema(**data)
    new_enrollment = create_enrollment(enrollment_data)
    return jsonify(EnrollmentResponseSchema.from_orm(new_enrollment).dict()), 201

@enrollments_bp.get("/class/<int:class_id>")
def get_enrollment_by_class_route(class_id):
    enrollment = get_enrollments_by_class(class_id)
    return jsonify([EnrollmentResponseSchema.from_orm(e).dict() for e in enrollment]), 200

@enrollments_bp.get("/member/<int:member_id>")
def get_enrollment_by_member_route(member_id):
    enrollment = get_enrollments_by_member(member_id)
    return jsonify([EnrollmentResponseSchema.from_orm(e).dict() for e in enrollment]), 200

@enrollments_bp.delete("/<int:enrollment_id>")
def cancel_enrollment_route(enrollment_id):
    cancel_enrollment(enrollment_id)
    return jsonify({"message": "Enrollment canceled"}), 200
