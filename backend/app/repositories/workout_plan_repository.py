from .base_repository import BaseRepository
from ..models.workout_plan import WorkoutPlan

class WorkoutPlanRepository(BaseRepository[WorkoutPlan]):
    def __init__(self, session):
        super().__init__(WorkoutPlan, session)

    def get_by_member(self, member_id: int):
        return self.session.query(WorkoutPlan).filter(WorkoutPlan.member_id == member_id).all()

    def get_by_trainer(self, trainer_id: int):
        return self.session.query(WorkoutPlan).filter(WorkoutPlan.trainer_id == trainer_id).all()
