from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import metadata

workout_plans = Table(
    "workout_plans", metadata,
    Column("id", Integer, primary_key=True),
    Column("member_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("trainer_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("title", String(100), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("is_active", Integer, nullable=False, default=1)  # 1 = active, 0 = archived
)
