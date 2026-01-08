from flask import Blueprint, request, jsonify, g
from backend.app.schemas.intake_evaluation import (
    IntakeEvaluationCreate, IntakeEvaluationUpdate, IntakeEvaluationResponse
)
from backend.app.services import intake_evaluation_service
from backend.app.utils.security import roles_required, token_required
from backend.app.utils.permissions import can_create_intake_evaluation

intake_evaluations_bp = Blueprint("intake_evaluations", __name__, url_prefix="/intake-evaluations")

@intake_evaluations_bp.post("/")
@token_required
def create_intake_evaluation_route():
    """Create a new intake evaluation (admin/trainer only)"""
    if not can_create_intake_evaluation(g.user):
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    evaluation_data = IntakeEvaluationCreate(**data)
    new_evaluation = intake_evaluation_service.create_intake_evaluation(evaluation_data)
    return jsonify(IntakeEvaluationResponse.from_orm(new_evaluation).dict()), 201

@intake_evaluations_bp.get("/member/<int:member_id>")
@token_required
def get_member_evaluations_route(member_id):
    """Get all evaluations for a specific member"""
    # TODO: Add permission check
    evaluations = intake_evaluation_service.get_evaluations_by_member(member_id)
    return jsonify([IntakeEvaluationResponse.from_orm(e).dict() for e in evaluations]), 200

@intake_evaluations_bp.get("/member/<int:member_id>/latest")
@token_required
def get_latest_evaluation_route(member_id):
    """Get most recent evaluation for a member"""
    evaluation = intake_evaluation_service.get_latest_evaluation(member_id)
    if not evaluation:
        return jsonify({"message": "No evaluation found"}), 404
    return jsonify(IntakeEvaluationResponse.from_orm(evaluation).dict()), 200

@intake_evaluations_bp.get("/<int:evaluation_id>")
@token_required
def get_evaluation_route(evaluation_id):
    """Get specific evaluation by ID"""
    evaluation = intake_evaluation_service.get_intake_evaluation_by_id(evaluation_id)
    return jsonify(IntakeEvaluationResponse.from_orm(evaluation).dict()), 200

@intake_evaluations_bp.put("/<int:evaluation_id>")
@token_required
def update_evaluation_route(evaluation_id):
    """Update an intake evaluation (admin/trainer only)"""
    if not can_create_intake_evaluation(g.user):
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    evaluation_data = IntakeEvaluationUpdate(**data)
    updated = intake_evaluation_service.update_intake_evaluation(evaluation_id, evaluation_data)
    return jsonify(IntakeEvaluationResponse.from_orm(updated).dict()), 200

@intake_evaluations_bp.get("/member/<int:member_id>/clearance")
@token_required
def check_clearance_route(member_id):
    """Check if member is cleared for training"""
    is_cleared = intake_evaluation_service.is_member_cleared_for_training(member_id)
    return jsonify({"member_id": member_id, "cleared_for_training": is_cleared}), 200
