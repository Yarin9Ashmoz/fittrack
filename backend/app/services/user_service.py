from backend.app.db.database import SessionLocal
from backend.app.repositories.user_repository import UserRepository
from backend.app import exceptions

def create_user(user_data):
    with SessionLocal() as session:
        repo = UserRepository(session)
        if repo.get_by_email(user_data.email):
            raise exceptions.DuplicateError("Email already registered")
        
        return repo.create(**user_data.dict())

def get_user_by_id(user_id: int):
    with SessionLocal() as session:
        user = UserRepository(session).get_by_id(user_id)
        if not user:
            raise exceptions.NotFoundError("User not found")
        return user

def get_all_users():
    with SessionLocal() as session:
        return UserRepository(session).get_all()

def update_user(user_id: int, user_data):
    with SessionLocal() as session:
        repo = UserRepository(session)
        update_data = {k: v for k, v in user_data.dict().items() if v is not None}
        updated = repo.update(user_id, **update_data)
        if not updated:
            raise exceptions.NotFoundError("User not found")
        return updated

def delete_user(user_id: int):
    with SessionLocal() as session:
        if not UserRepository(session).delete(user_id):
            raise exceptions.NotFoundError("User not found")
        return True
