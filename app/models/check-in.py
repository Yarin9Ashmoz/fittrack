from sqlalchemy import (
    Table, Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from app.db.database import metadata

check_in = Table(
    "check_in", metadata,
    Column("id", Integer, primary_key=True),
    Column("member_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("result", String(20), nullable=False),
    Column("reason", String(255), nullable=True)
)
