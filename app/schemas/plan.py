from pydantic import BaseModel

class PlanCreateSchema(BaseModel):
    name: str
    type: str
    price: float
    valid_days: int | None = None
    max_entries: int | None = None

class UpdatePlanSchema(BaseModel):
    name: str | None = None
    type: str | None = None
    price: float | None = None
    valid_days: int | None = None
    max_entries: int | None = None

class PlanResponseSchema(BaseModel):
    id: int
    name: str
    type: str
    price: float
    valid_days: int | None
    max_entries: int | None

    class Config:
        orm_mode = True