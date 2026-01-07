from backend.app.db.database import SessionLocal
from backend.app.repositories.class_session_repository import ClassSessionRepository
from backend.app import exceptions

def create_class(data: dict):
    with SessionLocal() as session:
        return ClassSessionRepository(session).create(**data)

def get_class_by_id(session_id: int):
    with SessionLocal() as session:
        row = ClassSessionRepository(session).get_by_id(session_id)
        if not row:
            raise exceptions.NotFoundError("Class session not found")
        return row

def get_all_classes():
    with SessionLocal() as session:
        return ClassSessionRepository(session).get_all()

def update_class(session_id: int, data: dict):
    with SessionLocal() as session:
        updated = ClassSessionRepository(session).update(session_id, **data)
        if not updated:
            raise exceptions.NotFoundError("Class session not found")
        return updated

def delete_class(session_id: int):
    with SessionLocal() as session:
        if not ClassSessionRepository(session).delete(session_id):
            raise exceptions.NotFoundError("Class session not found")
        return True
