from app.db.database import engine
from app.models.users import users
from app.exceptions import NotFoundError, DuplicateError

def create_user(user_data):
    with engine.connect() as conn:
        query = users.select().where(users.c.email == user_data.email)
        existing = conn.execute(query).fetchone()
        if existing:
            raise DuplicateError("Email already exists")

        insert_query = users.insert().values(**user_data.dict())
        result = conn.execute(insert_query)
        user_id = result.lastrowid

        return get_user_by_id(user_id)


def get_user_by_id(user_id: int):
    with engine.connect() as conn:
        query = users.select().where(users.c.id == user_id)
        user = conn.execute(query).fetchone()

        if not user:
            raise NotFoundError("User not found")

        return user


def get_all_users():
    with engine.connect() as conn:
        query = users.select()
        return conn.execute(query).fetchall()


def update_user(user_id: int, user_data):
    with engine.connect() as conn:
        user = get_user_by_id(user_id)

        if user_data.email:
            query = users.select().where(users.c.email == user_data.email)
            existing = conn.execute(query).fetchone()

            if existing and existing.id != user_id:
                raise DuplicateError("Email already exists")

        update_data = {k: v for k, v in user_data.dict().items() if v is not None}

        update_query = users.update().where(users.c.id == user_id).values(**update_data)
        conn.execute(update_query)

        return get_user_by_id(user_id)


def delete_user(user_id: int):
    with engine.connect() as conn:
        get_user_by_id(user_id)

        delete_query = users.delete().where(users.c.id == user_id)
        conn.execute(delete_query)

        return {"message": "User deleted"}
