from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class PaymentCreateSchema(BaseModel):
    member_id: int
    payment_method: str = "manual"  # closed_lesson, subscription, manual
    subscription_id: Optional[int] = None
    class_session_id: Optional[int] = None
    calculated_amount: Decimal
    discount_applied: Decimal = Decimal("0.00")
    amount: float  # Final amount after discount
    reference: Optional[str] = None

class PaymentResponseSchema(BaseModel):
    id: int
    member_id: int
    subscription_id: Optional[int]
    class_session_id: Optional[int]
    payment_method: str
    calculated_amount: Decimal
    discount_applied: Decimal
    amount: float
    status: str
    paid_at: Optional[datetime]
    reference: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}

