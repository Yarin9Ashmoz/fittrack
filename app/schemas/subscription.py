from pydantic import BaseModel
from datetime import date


class SubscriptionCreateSchema(BaseModel):
    user_id: int
    plan_id: int
    status: str = "active"
    start_date: date
    end_date: date
    remaining_entries: int | None = None
    frozen_until: str | None = None

class UpdateSubscriptionSchema(BaseModel):
    plan_id: int | None = None
    status: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    remaining_entries: int | None = None
    frozen_until: str | None = None

class SubscriptionResponseSchema(BaseModel):
    id: int
    user_id: int
    plan_id: int
    status: str
    start_date: date
    end_date: date
    remaining_entries: int | None
    frozen_until: str | None

    class Config:
        orm_mode = True