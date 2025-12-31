from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, text
from backend.app.db.database import metadata

class_sessions = Table(
    "class_sessions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(100), nullable=False),
    Column("starts_at", DateTime, nullable=False),
    Column("capacity", Integer, nullable=False),
    Column("trainer_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("status", String(20), nullable=False, server_default=text("'active'"))
)
