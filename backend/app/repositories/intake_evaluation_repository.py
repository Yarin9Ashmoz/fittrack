from backend.app.repositories.base_repository import BaseRepository
from backend.app.models.intake_evaluation import IntakeEvaluation
from sqlalchemy.orm import Session

class IntakeEvaluationRepository(BaseRepository[IntakeEvaluation]):
    def __init__(self, session: Session):
        super().__init__(IntakeEvaluation, session)

    def get_all(self):
        """Get all intake evaluations"""
        return self.session.query(self.model).all() 
    
    def get_by_member_id(self, member_id: int):
        """Get all evaluations for a specific member"""
        return self.session.query(self.model).filter(
            self.model.member_id == member_id
        ).order_by(self.model.evaluation_date.desc()).all()
    
    def get_latest_by_member(self, member_id: int):
        """Get the most recent evaluation for a member"""
        return self.session.query(self.model).filter(
            self.model.member_id == member_id
        ).order_by(self.model.evaluation_date.desc()).first()
