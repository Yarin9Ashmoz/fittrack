from sqlalchemy import (
    Table, Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from backend.app.db.database import metadata

checkins = Table(
    "checkins", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("member_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("subscription_id", Integer, ForeignKey("subscriptions.id"), nullable=False),
    Column("class_id", Integer, ForeignKey("class_sessions.id"), nullable=True),
    Column("timestamp", DateTime, server_default=func.now())
)

