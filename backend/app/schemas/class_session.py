from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ClassCreateSchema(BaseModel):
    title: str
    starts_at: datetime
    ends_at: Optional[datetime] = None
    capacity: int
    trainer_id: int


class ClassUpdateSchema(BaseModel):
    title: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    capacity: Optional[int] = None
    trainer_id: Optional[int] = None
    status: Optional[str] = None
    is_registration_closed: Optional[bool] = None


class ClassResponseSchema(BaseModel):
    id: int
    title: str
    starts_at: datetime
    ends_at: Optional[datetime]
    capacity: int
    trainer_id: int
    status: str
    is_registration_closed: bool

    enrolled_count: Optional[int] = None
    waitlist_count: Optional[int] = None

    model_config = {"from_attributes": True}
