from backend.app.db.database import SessionLocal
from backend.app.repositories.intake_evaluation_repository import IntakeEvaluationRepository
from backend.app import exceptions

def create_intake_evaluation(evaluation_data):
    """Create a new intake evaluation"""
    with SessionLocal() as session:
        repo = IntakeEvaluationRepository(session)
        return repo.create(**evaluation_data.dict())

def get_intake_evaluation_by_id(evaluation_id: int):
    """Get intake evaluation by ID"""
    with SessionLocal() as session:
        evaluation = IntakeEvaluationRepository(session).get_by_id(evaluation_id)
        if not evaluation:
            raise exceptions.NotFoundError("Intake evaluation not found")
        return evaluation

def get_evaluations_by_member(member_id: int):
    """Get all evaluations for a member"""
    with SessionLocal() as session:
        return IntakeEvaluationRepository(session).get_by_member_id(member_id)

def get_latest_evaluation(member_id: int):
    """Get most recent evaluation for a member"""
    with SessionLocal() as session:
        return IntakeEvaluationRepository(session).get_latest_by_member(member_id)

def update_intake_evaluation(evaluation_id: int, evaluation_data):
    """Update an existing intake evaluation"""
    with SessionLocal() as session:
        repo = IntakeEvaluationRepository(session)
        update_data = {k: v for k, v in evaluation_data.dict().items() if v is not None}
        updated = repo.update(evaluation_id, **update_data)
        if not updated:
            raise exceptions.NotFoundError("Intake evaluation not found")
        return updated

def is_member_cleared_for_training(member_id: int):
    """Check if member is cleared for training based on latest evaluation"""
    with SessionLocal() as session:
        latest = IntakeEvaluationRepository(session).get_latest_by_member(member_id)
        if not latest:
            return False  # No evaluation = not cleared
        return latest.cleared_for_training
