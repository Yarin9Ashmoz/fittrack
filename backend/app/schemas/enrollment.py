from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EnrollmentCreateSchema(BaseModel):
    member_id: int
    class_id: int


class EnrollmentResponseSchema(BaseModel):
    id: int
    member_id: int
    class_id: int
    created_at: datetime
    status: str

    waitlist_position: Optional[int] = None
    promoted_at: Optional[datetime] = None
    deadline_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None

    model_config = {"from_attributes": True}
