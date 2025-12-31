from sqlalchemy import Table, Column, Integer, String, ForeignKey
from backend.app.db.database import metadata

workout_items = Table(
    "exercise", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("plan_id", Integer, ForeignKey("workout_plans.id"), nullable=False),
    Column("exercise_name", String(50), nullable=False),
    Column("sets", Integer, nullable=False),
    Column("reps", Integer, nullable=False),
    Column("target_weight", Integer, nullable=True),
    Column("notes", String(255), nullable=True)
)
