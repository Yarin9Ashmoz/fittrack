from .base_repository import BaseRepository
from ..models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(User, session)

    def get_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()
