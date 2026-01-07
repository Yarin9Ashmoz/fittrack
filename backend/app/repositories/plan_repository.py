from .base_repository import BaseRepository
from ..models.plan import Plan

class PlanRepository(BaseRepository[Plan]):
    def __init__(self, session):
        super().__init__(Plan, session)
