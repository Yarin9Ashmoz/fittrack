from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

# Enums for error report
class ErrorSeverity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class ErrorStatus(str, Enum):
    new = "new"
    investigating = "investigating"
    resolved = "resolved"
    ignored = "ignored"

# Error Report Schemas
class ErrorReportCreate(BaseModel):
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    url: Optional[str] = None
    user_id: Optional[int] = None
    severity: ErrorSeverity = ErrorSeverity.medium

class ErrorReportUpdate(BaseModel):
    status: Optional[ErrorStatus] = None
    resolved_by_id: Optional[int] = None
    notes: Optional[str] = None

class ErrorReportResponse(BaseModel):
    id: int
    error_type: str
    error_message: str
    stack_trace: Optional[str]
    occurred_at: datetime
    url: Optional[str]
    user_id: Optional[int]
    severity: ErrorSeverity
    status: ErrorStatus
    resolved_by_id: Optional[int]
    resolved_at: Optional[datetime]
    notes: Optional[str]

    model_config = {"from_attributes": True}
