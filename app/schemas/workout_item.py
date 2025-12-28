from pydantic import BaseModel, EmailStr, Field

class WorkoutItemCreateSchema(BaseModel):
    plan_id: int
    exercise_name: str
    sets: int | None = None
    reps: int | None = None
    target_weight: float | None = None
    notes: str | None = None

class WorkoutItemUpdateSchema(BaseModel):
    exercise_name: str | None = None
    sets: int | None = None
    reps: int | None = None
    target_weight: float | None = None
    notes: str | None = None

class WorkoutItemResponseSchema(BaseModel):
    id: int
    plan_id: int
    exercise_name: str
    sets: int | None
    reps: int | None
    target_weight: float | None
    notes: str | None

    class Config:
        orm_mode = True