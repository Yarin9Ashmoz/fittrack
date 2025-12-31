from sqlalchemy import Table, Column, Integer, String
from backend.app.db.database import metadata

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(50), nullable=False),
    Column("last_name", String(50), nullable=False),
    Column("email", String(100), nullable=False, unique=True),
    Column("phone", String(20), nullable=False),
    Column("address", String(255)),
    Column("role", String(20), nullable=False),
    Column("status", String(20), nullable=False, default="active")
)
