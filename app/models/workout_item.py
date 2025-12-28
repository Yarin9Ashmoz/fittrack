from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from app.db.database import metadata

workout_items = Table(
    "workout_items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("plan_id", Integer, ForeignKey("workout_plans.id"), nullable=False),
    Column("exercise_name", String(100), nullable=False),
    Column("sets", Integer, nullable=True),
    Column("reps", Integer, nullable=True),
    Column("target_weight", Float, nullable=True),
    Column("notes", String(255), nullable=True)
)
