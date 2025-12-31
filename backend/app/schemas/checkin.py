from pydantic import BaseModel
from datetime import datetime


class CheckinCreateSchema(BaseModel):
    member_id: int
    class_id: int | None = None


class CheckinResponseSchema(BaseModel):
    id: int
    member_id: int
    subscription_id: int
    class_id: int | None
    timestamp: datetime

    model_config = {"from_attributes": True}

