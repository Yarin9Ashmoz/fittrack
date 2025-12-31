from flask import Blueprint, request, jsonify
from backend.app.schemas.checkin import CheckinCreateSchema, CheckinResponseSchema
from backend.app.services.checkin_service import (
    create_checkin,
    get_checkins_by_member,
    get_all_checkins
)

checkins_bp = Blueprint("checkins", __name__, url_prefix="/checkins")

@checkins_bp.get("/")
def get_all_checkins_route():
    checkins = get_all_checkins()
    return jsonify([CheckinResponseSchema.from_orm(c).dict() for c in checkins]), 200

# יצירת Check-in חדש
@checkins_bp.post("/")
def create_checkin_route():
    data = request.get_json()
    checkin_data = CheckinCreateSchema(**data)
    new_checkin = create_checkin(checkin_data.member_id, checkin_data.class_id)
    return jsonify(CheckinResponseSchema.from_orm(new_checkin).dict()), 201


# היסטוריית כניסות של מתאמן
@checkins_bp.get("/member/<int:member_id>")
def get_member_checkins_route(member_id):
    checkins = get_checkins_by_member(member_id)
    return jsonify([CheckinResponseSchema.from_orm(c).dict() for c in checkins]), 200
