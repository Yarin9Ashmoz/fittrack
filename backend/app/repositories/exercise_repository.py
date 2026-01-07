from .base_repository import BaseRepository
from ..models.exercise import Exercise

class ExerciseRepository(BaseRepository[Exercise]):
    def __init__(self, session):
        super().__init__(Exercise, session)
