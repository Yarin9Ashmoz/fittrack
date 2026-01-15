from typing import Optional
from abc import ABC, abstractmethod
from backend.app.db.database import SessionLocal
from backend.app.repositories.user_repository import UserRepository
from backend.app import exceptions


class UserService(ABC):
    """Abstract base UserService. All role-services inherit from this."""

    def __init__(self, session=None, current_user=None):
        self._external_session = session
        self.current_user = current_user

    def _get_session(self):
        return self._external_session or SessionLocal()

    @property
    @abstractmethod
    def role_name(self) -> Optional[str]:
        """Role name this service represents (e.g., 'admin', 'trainer', 'member')."""
        raise NotImplementedError

    # Common CRUD helpers
    def get_by_id(self, user_id: int):
        with self._get_session() as session:
            repo = UserRepository(session)
            user = repo.get_by_id(user_id)
            if not user:
                raise exceptions.NotFoundError("User not found")
            return user

    def get_all(self):
        with self._get_session() as session:
            repo = UserRepository(session)
            return repo.get_all()

    def get_by_email(self, email: str):
        with self._get_session() as session:
            repo = UserRepository(session)
            return repo.get_by_email(email)

    def create(self, **user_data):
        with self._get_session() as session:
            repo = UserRepository(session)
            if repo.get_by_email(user_data.get("email")):
                raise exceptions.DuplicateError("Email already registered")
            return repo.create(**user_data)

    def update(self, user_id: int, **user_data):
        with self._get_session() as session:
            repo = UserRepository(session)
            updated = repo.update(user_id, **user_data)
            if not updated:
                raise exceptions.NotFoundError("User not found")
            return updated

    def delete(self, user_id: int):
        with self._get_session() as session:
            repo = UserRepository(session)
            if not repo.delete(user_id):
                raise exceptions.NotFoundError("User not found")
            return True


class GenericUserService(UserService):
    """Concrete default User service for non-role-specific usage."""

    @property
    def role_name(self) -> Optional[str]:
        return "user"


# Backwards-compatible function interfaces (used by existing endpoints)
def create_user(user_data):
    svc = GenericUserService()
    return svc.create(**user_data.dict())


def get_user_by_id(user_id: int):
    svc = GenericUserService()
    return svc.get_by_id(user_id)


def get_all_users():
    svc = GenericUserService()
    return svc.get_all()


def update_user(user_id: int, user_data):
    svc = GenericUserService()
    update_data = {k: v for k, v in user_data.dict().items() if v is not None}
    return svc.update(user_id, **update_data)

def change_user_status(user_id: int, status: bool):
    svc = GenericUserService()
    return svc.update(user_id, status=status)

def delete_user(user_id: int):
    svc = GenericUserService()
    return svc.delete(user_id)
