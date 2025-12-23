from sqlalchemy import (
    Table, Column, Integer, String, DateTime, ForeignKey, Float
)
from sqlalchemy.sql import func
from app.db.database import metadata

payments = Table(
    "payments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("subscription_id", Integer, ForeignKey("subscriptions.id"), nullable=False),
    Column("amount", Float, nullable=False),
    Column("status", String(20), nullable=False, default="pending"),
    Column("paid_at", DateTime, server_default=func.now()),
    Column("reference", String(100), nullable=True)
)
