from flask import Blueprint, request, jsonify
from backend.app.schemas.enrollment import (
    EnrollmentCreateSchema,
    EnrollmentResponseSchema
)
from backend.app.services.enrollment_service import (
    create_enrollment,
    get_enrollments_by_class,
    get_enrollments_by_member,
    cancel_enrollment,
    get_all_enrollments,
    confirm_promotion,
    expire_promotions
)

enrollments_bp = Blueprint("enrollments", __name__, url_prefix="/enrollments")


# ----------------------------------------------------
# 1. כל ההרשמות
# ----------------------------------------------------
@enrollments_bp.get("/")
def get_all_enrollments_route():
    enrollments = get_all_enrollments()
    return jsonify([EnrollmentResponseSchema.from_orm(e).dict() for e in enrollments]), 200


# ----------------------------------------------------
# 2. יצירת הרשמה (כולל תור)
# ----------------------------------------------------
@enrollments_bp.post("/")
def create_enrollment_route():
    data = request.get_json()
    enrollment_data = EnrollmentCreateSchema(**data)
    new_enrollment = create_enrollment(enrollment_data.dict())
    return jsonify(EnrollmentResponseSchema.from_orm(new_enrollment).dict()), 201


# ----------------------------------------------------
# 3. כל ההרשמות לשיעור
# ----------------------------------------------------
@enrollments_bp.get("/class/<int:class_id>")
def get_enrollment_by_class_route(class_id):
    enrollment = get_enrollments_by_class(class_id)
    return jsonify([EnrollmentResponseSchema.from_orm(e).dict() for e in enrollment]), 200


# ----------------------------------------------------
# 4. כל ההרשמות של מתאמן
# ----------------------------------------------------
@enrollments_bp.get("/member/<int:member_id>")
def get_enrollment_by_member_route(member_id):
    enrollment = get_enrollments_by_member(member_id)
    return jsonify([EnrollmentResponseSchema.from_orm(e).dict() for e in enrollment]), 200


# ----------------------------------------------------
# 5. ביטול הרשמה (כולל קידום מהתור)
# ----------------------------------------------------
@enrollments_bp.delete("/<int:enrollment_id>")
def cancel_enrollment_route(enrollment_id):
    cancel_enrollment(enrollment_id)
    return jsonify({"message": "Enrollment canceled"}), 200


# ----------------------------------------------------
# 6. אישור קידום מהתור
# ----------------------------------------------------
@enrollments_bp.post("/<int:enrollment_id>/confirm")
def confirm_promotion_route(enrollment_id):
    updated = confirm_promotion(enrollment_id)
    return jsonify(EnrollmentResponseSchema.from_orm(updated).dict()), 200


# ----------------------------------------------------
# 7. ניקוי קידומים שפג תוקפם
# ----------------------------------------------------
@enrollments_bp.post("/expire-promotions")
def expire_promotions_route():
    expired = expire_promotions()
    return jsonify({
        "expired": [EnrollmentResponseSchema.from_orm(e).dict() for e in expired]
    }), 200
