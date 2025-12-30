from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.sql import func
from app.db.database import metadata

subscriptions = Table(
    "subscriptions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("users_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("plan_id", Integer, ForeignKey("plans.id"), nullable=False),
    Column("status", String(20), nullable=False, default="active"),
    Column("start_date", Date, nullable=False),
    Column("end_date", Date, nullable=False),
    Column("remaining_entries", Integer, nullable=True),
    Column("frozen_until", Date, nullable=True),
    Column("created_at", Date, server_default=func.current_date())
)
