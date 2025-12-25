from pydantic import BaseModel
from datetime import datetime

class PaymentCreateSchema(BaseModel):
    subscription_id: int
    amount: float
    reference: str

class PaymentResponseSchema(BaseModel):
    id: int
    subscription_id: int
    amount: float
    status: str
    paid_at: datetime
    reference: str

    class config:
        orm_mode = True


