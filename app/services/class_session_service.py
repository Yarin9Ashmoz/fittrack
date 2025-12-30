from app.db.database import engine
from app.models.class_session import class_sessions
from app import exceptions
from sqlalchemy import select, update, delete


def create_class(data: dict):
    with engine.connect() as conn:
        insert_query = class_sessions.insert().values(**data)
        result = conn.execute(insert_query)
        new_id = result.lastrowid
        return get_class_by_id(new_id)


def get_all_classes():
    with engine.connect() as conn:
        query = select(class_sessions)
        return conn.execute(query).fetchall()


def get_class_by_id(class_id: int):
    with engine.connect() as conn:
        query = select(class_sessions).where(class_sessions.c.id == class_id)
        row = conn.execute(query).fetchone()

        if not row:
            raise exceptions.NotFoundError("Class not found")

        return row


def update_class(class_id: int, data: dict):
    with engine.connect() as conn:
        get_class_by_id(class_id)

        update_query = (
            update(class_sessions)
            .where(class_sessions.c.id == class_id)
            .values(**data)
        )
        conn.execute(update_query)

        return get_class_by_id(class_id)


def delete_class(class_id: int):
    with engine.connect() as conn:
        get_class_by_id(class_id)
        delete_query = delete(class_sessions).where(class_sessions.c.id == class_id)
        conn.execute(delete_query)
