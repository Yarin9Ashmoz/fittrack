from pydantic import BaseModel
from datetime import datetime

class EnrollmentCreateSchema(BaseModel):
    member_id: int
    class_id: int


class EnrollmentResponseSchema(BaseModel):
    id: int
    member_id: int
    class_id: int
    created_at: datetime
    status: str
