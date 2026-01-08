from flask import Blueprint, request, jsonify
from backend.app.schemas.error_report import (
    ErrorReportCreate, ErrorReportUpdate, ErrorReportResponse
)
from backend.app.services import error_report_service
from backend.app.utils.security import roles_required, token_required
from backend.app.utils.permissions import can_manage_errors

error_reports_bp = Blueprint("error_reports", __name__, url_prefix="/error-reports")

@error_reports_bp.get("/")
@token_required
@roles_required('admin')
def get_all_errors_route():
    """Get all error reports (admin only)"""
    status_filter = request.args.get('status')
    severity_filter = request.args.get('severity')
    
    if status_filter:
        errors = error_report_service.get_errors_by_status(status_filter)
    elif severity_filter:
        errors = error_report_service.get_errors_by_severity(severity_filter)
    else:
        errors = error_report_service.get_all_errors()
    
    return jsonify([ErrorReportResponse.from_orm(e).dict() for e in errors]), 200

@error_reports_bp.get("/unresolved")
@token_required
@roles_required('admin')
def get_unresolved_errors_route():
    """Get all unresolved errors (admin only)"""
    errors = error_report_service.get_unresolved_errors()
    return jsonify([ErrorReportResponse.from_orm(e).dict() for e in errors]), 200

@error_reports_bp.get("/stats")
@token_required
@roles_required('admin')
def get_error_stats_route():
    """Get error statistics for dashboard (admin only)"""
    stats = error_report_service.get_error_stats()
    return jsonify(stats), 200

@error_reports_bp.get("/<int:error_id>")
@token_required
@roles_required('admin')
def get_error_report_route(error_id):
    """Get specific error report by ID (admin only)"""
    error = error_report_service.get_error_report_by_id(error_id)
    return jsonify(ErrorReportResponse.from_orm(error).dict()), 200

@error_reports_bp.put("/<int:error_id>")
@token_required
@roles_required('admin')
def update_error_status_route(error_id):
    """Update error status (admin only)"""
    from flask import g
    data = request.get_json()
    
    # Add current user as resolver if marking as resolved
    if data.get('status') == 'resolved' and 'resolved_by_id' not in data:
        data['resolved_by_id'] = g.user.id
    
    error_data = ErrorReportUpdate(**data)
    updated = error_report_service.update_error_status(error_id, error_data)
    return jsonify(ErrorReportResponse.from_orm(updated).dict()), 200
