from datetime import datetime
from pydantic import BaseModel

class WorkoutPlanCreateSchema(BaseModel):
    member_id: int
    trainer_id: int | None = None
    title: str
    is_active: bool | None = True

class WorkoutPlanUpdateSchema(BaseModel):
    member_id: int | None = None
    trainer_id: int | None = None
    title: str | None = None
    is_active: bool | None = True

class WorkoutPlanResponseSchema(BaseModel):
    id: int
    member_id: int
    trainer_id: int
    title: str
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}

