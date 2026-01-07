from .base_repository import BaseRepository
from ..models.checkin import Checkin

class CheckinRepository(BaseRepository[Checkin]):
    def __init__(self, session):
        super().__init__(Checkin, session)
