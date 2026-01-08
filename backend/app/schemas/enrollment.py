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

    # Original fields (some may be deprecated)
    waitlist_position: Optional[int] = None
    promoted_at: Optional[datetime] = None
    deadline_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None
    
    # New waitlist management fields
    enrolled_at: Optional[datetime] = None
    waitlist_joined_at: Optional[datetime] = None
    promotion_attempted_at: Optional[datetime] = None
    promotion_method: Optional[str] = None  # auto, api, manual

    model_config = {"from_attributes": True}

