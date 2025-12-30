from pydantic import BaseModel
from datetime import datetime

class ClassCreateSchema(BaseModel):
    title: str
    starts_at: datetime
    capacity: int
    trainer_id: int


class ClassUpdateSchema(BaseModel):
    title: str | None = None
    starts_at: datetime | None = None
    capacity: int | None = None
    trainer_id: int | None = None
    status: str | None = None


class ClassResponseSchema(BaseModel):
    id: int
    title: str
    starts_at: datetime
    capacity: int
    trainer_id: int
    status: str

    class Config:
        orm_mode = False
