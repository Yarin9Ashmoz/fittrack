from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

# Personal Tracking Schemas
class PersonalTrackingCreate(BaseModel):
    member_id: int
    emotional_regulation: Optional[Dict[str, Any]] = None
    symptom_tracking: Optional[Dict[str, Any]] = None
    social_function: Optional[Dict[str, Any]] = None
    physical_function: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    recorded_by_id: int

class PersonalTrackingUpdate(BaseModel):
    emotional_regulation: Optional[Dict[str, Any]] = None
    symptom_tracking: Optional[Dict[str, Any]] = None
    social_function: Optional[Dict[str, Any]] = None
    physical_function: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

class PersonalTrackingResponse(BaseModel):
    id: int
    member_id: int
    tracking_date: datetime
    emotional_regulation: Optional[Dict[str, Any]]
    symptom_tracking: Optional[Dict[str, Any]]
    social_function: Optional[Dict[str, Any]]
    physical_function: Optional[Dict[str, Any]]
    notes: Optional[str]
    recorded_by_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
