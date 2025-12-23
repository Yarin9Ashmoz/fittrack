from sqlalchemy import Table, Column, Integer, String, Float
from app.db.database import metadata

plans = Table(
    "plans",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("type", String(20), nullable=False),
    Column("price", Float, nullable=False),
    Column("valid_days", Integer, nullable=True),
    Column("max_entries", Integer, nullable=True)
)
