from backend.app.repositories.base_repository import BaseRepository
from backend.app.models.error_report import ErrorReport
from sqlalchemy.orm import Session

class ErrorReportRepository(BaseRepository[ErrorReport]):
    def __init__(self, session: Session):
        super().__init__(ErrorReport, session)
    
    def get_by_status(self, status: str):
        """Get all error reports by status"""
        return self.session.query(self.model).filter(
            self.model.status == status
        ).order_by(self.model.occurred_at.desc()).all()
    
    def get_by_severity(self, severity: str):
        """Get all error reports by severity"""
        return self.session.query(self.model).filter(
            self.model.severity == severity
        ).order_by(self.model.occurred_at.desc()).all()
    
    def get_unresolved(self):
        """Get all unresolved errors"""
        return self.session.query(self.model).filter(
            self.model.status.in_(["new", "investigating"])
        ).order_by(self.model.severity.desc(), self.model.occurred_at.desc()).all()
