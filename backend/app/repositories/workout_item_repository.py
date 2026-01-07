from .base_repository import BaseRepository
from ..models.workout_item import WorkoutItem

class WorkoutItemRepository(BaseRepository[WorkoutItem]):
    def __init__(self, session):
        super().__init__(WorkoutItem, session)

    def get_by_plan(self, plan_id: int):
        return self.session.query(WorkoutItem).filter(WorkoutItem.plan_id == plan_id).all()
