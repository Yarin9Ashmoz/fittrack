from sqlalchemy import Table, Column, Integer, DateTime, ForeignKey, String
from datetime import datetime
from app.db.database import metadata

enrollments = Table(
    "enrollments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("member_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("class_id", Integer, ForeignKey("class_sessions.id"), nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("status", String(20), default="active", nullable=False)
)
