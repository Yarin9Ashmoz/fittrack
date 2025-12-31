from pydantic import BaseModel
from datetime import date
from typing import Optional


class SubscriptionCreateSchema(BaseModel):
    user_id: int
    plan_id: int
    remaining_entries: Optional[int] = None


class SubscriptionUpdateSchema(BaseModel):
    # עדכון כללי של מנוי (אם תרצה בעתיד)
    plan_id: Optional[int] = None
    remaining_entries: Optional[int] = None


class SubscriptionUpdateEntriesSchema(BaseModel):
    remaining_entries: int

class SubscriptionFreezeSchema(BaseModel):
    frozen_until: date

class SubscriptionResponseSchema(BaseModel):
    id: int
    user_id: int
    plan_id: int
    status: str
    start_date: date
    end_date: date
    remaining_entries: Optional[int]
    frozen_until: Optional[date]

    model_config = {"from_attributes": True}
