from flask import Blueprint, request, jsonify, g
from backend.app.schemas.personal_tracking import (
    PersonalTrackingCreate, PersonalTrackingUpdate, PersonalTrackingResponse
)
from backend.app.services import personal_tracking_service
from backend.app.utils.security import token_required
from backend.app.utils.permissions import can_view_personal_tracking
from datetime import datetime, timedelta

personal_tracking_bp = Blueprint("personal_tracking", __name__, url_prefix="/personal-tracking")

@personal_tracking_bp.post("/")
@token_required
def create_tracking_entry_route():
    """Create a new personal tracking entry"""
    data = request.get_json()
    tracking_data = PersonalTrackingCreate(**data)
    
    # Members can only track themselves, trainers can track their students
    if not can_view_personal_tracking(g.user, tracking_data.member_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    new_entry = personal_tracking_service.create_tracking_entry(tracking_data)
    return jsonify(PersonalTrackingResponse.from_orm(new_entry).dict()), 201

@personal_tracking_bp.get("/member/<int:member_id>")
@token_required
def get_member_tracking_route(member_id):
    """Get all tracking entries for a member"""
    if not can_view_personal_tracking(g.user, member_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    entries = personal_tracking_service.get_tracking_by_member(member_id)
    return jsonify([PersonalTrackingResponse.from_orm(e).dict() for e in entries]), 200

@personal_tracking_bp.get("/member/<int:member_id>/summary")
@token_required
def get_tracking_summary_route(member_id):
    """Get summary of tracking for the last N days"""
    if not can_view_personal_tracking(g.user, member_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    days = request.args.get('days', 30, type=int)
    summary = personal_tracking_service.get_tracking_summary(member_id, days)
    
    # Convert entries to response schema
    summary['entries'] = [PersonalTrackingResponse.from_orm(e).dict() for e in summary['entries']]
    
    return jsonify(summary), 200

@personal_tracking_bp.get("/<int:tracking_id>")
@token_required
def get_tracking_entry_route(tracking_id):
    """Get specific tracking entry by ID"""
    entry = personal_tracking_service.get_tracking_entry_by_id(tracking_id)
    
    if not can_view_personal_tracking(g.user, entry.member_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    return jsonify(PersonalTrackingResponse.from_orm(entry).dict()), 200

@personal_tracking_bp.put("/<int:tracking_id>")
@token_required
def update_tracking_entry_route(tracking_id):
    """Update a tracking entry"""
    entry = personal_tracking_service.get_tracking_entry_by_id(tracking_id)
    
    if not can_view_personal_tracking(g.user, entry.member_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    tracking_data = PersonalTrackingUpdate(**data)
    updated = personal_tracking_service.update_tracking_entry(tracking_id, tracking_data)
    return jsonify(PersonalTrackingResponse.from_orm(updated).dict()), 200
