from pydantic import BaseModel
from datetime import datetime


class CheckinCreateSchema(BaseModel):
    member_id: int
    class_id: int | None = None


class CheckinResponseSchema(BaseModel):
    id: int
    member_id: int
    class_id: int | None
    timestamp: datetime

    class Config:
        orm_mode = True
