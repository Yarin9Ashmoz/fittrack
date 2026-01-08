from backend.app.db.database import SessionLocal
from backend.app.repositories.error_report_repository import ErrorReportRepository
from backend.app import exceptions
from datetime import datetime
import traceback
import logging

# Configure logging
logger = logging.getLogger(__name__)

def create_error_report(error_data):
    """Create a new error report"""
    with SessionLocal() as session:
        repo = ErrorReportRepository(session)
        return repo.create(**error_data.dict())

def log_error(error_type: str, error_message: str, severity: str = "medium", 
              url: str = None, user_id: int = None, stack_trace: str = None):
    """
    Log an error to the database and trigger monitoring service alert
    This is the main function to be called throughout the app for error logging
    """
    try:
        with SessionLocal() as session:
            repo = ErrorReportRepository(session)
            error_report = repo.create(
                error_type=error_type,
                error_message=error_message,
                severity=severity,
                url=url,
                user_id=user_id,
                stack_trace=stack_trace or traceback.format_exc()
            )
            
            # TODO: Send to monitoring service (Sentry) based on severity
            if severity in ["high", "critical"]:
                logger.critical(f"Critical error logged: {error_type} - {error_message}")
                # send_to_monitoring_service(error_report)
            
            return error_report
    except Exception as e:
        # If error logging fails, at least log to console
        logger.error(f"Failed to log error to database: {str(e)}")
        return None

def get_error_report_by_id(error_id: int):
    """Get error report by ID"""
    with SessionLocal() as session:
        error = ErrorReportRepository(session).get_by_id(error_id)
        if not error:
            raise exceptions.NotFoundError("Error report not found")
        return error

def get_all_errors():
    """Get all error reports"""
    with SessionLocal() as session:
        return ErrorReportRepository(session).get_all()

def get_errors_by_status(status: str):
    """Get errors by status"""
    with SessionLocal() as session:
        return ErrorReportRepository(session).get_by_status(status)

def get_errors_by_severity(severity: str):
    """Get errors by severity"""
    with SessionLocal() as session:
        return ErrorReportRepository(session).get_by_severity(severity)

def get_unresolved_errors():
    """Get all unresolved errors"""
    with SessionLocal() as session:
        return ErrorReportRepository(session).get_unresolved()

def update_error_status(error_id: int, error_data):
    """Update error status (for admin)"""
    with SessionLocal() as session:
        repo = ErrorReportRepository(session)
        update_data = {k: v for k, v in error_data.dict().items() if v is not None}
        
        # Set resolved_at if status is resolved
        if update_data.get("status") == "resolved" and "resolved_at" not in update_data:
            update_data["resolved_at"] = datetime.now()
        
        updated = repo.update(error_id, **update_data)
        if not updated:
            raise exceptions.NotFoundError("Error report not found")
        return updated

def get_error_stats():
    """Get error statistics for dashboard"""
    with SessionLocal() as session:
        repo = ErrorReportRepository(session)
        all_errors = repo.get_all()
        
        stats = {
            "total": len(all_errors),
            "by_status": {},
            "by_severity": {},
            "unresolved": len(repo.get_unresolved())
        }
        
        for error in all_errors:
            stats["by_status"][error.status] = stats["by_status"].get(error.status, 0) + 1
            stats["by_severity"][error.severity] = stats["by_severity"].get(error.severity, 0) + 1
        
        return stats
