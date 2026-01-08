from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

# Intake Evaluation Schemas
class IntakeEvaluationCreate(BaseModel):
    member_id: int
    mental_status: Optional[Dict[str, Any]] = None
    cognitive_function: Optional[Dict[str, Any]] = None
    physical_limitations: Optional[Dict[str, Any]] = None
    cleared_for_training: bool = False
    notes: Optional[str] = None
    evaluated_by_id: int

class IntakeEvaluationUpdate(BaseModel):
    mental_status: Optional[Dict[str, Any]] = None
    cognitive_function: Optional[Dict[str, Any]] = None
    physical_limitations: Optional[Dict[str, Any]] = None
    cleared_for_training: Optional[bool] = None
    notes: Optional[str] = None

class IntakeEvaluationResponse(BaseModel):
    id: int
    member_id: int
    evaluation_date: datetime
    mental_status: Optional[Dict[str, Any]]
    cognitive_function: Optional[Dict[str, Any]]
    physical_limitations: Optional[Dict[str, Any]]
    cleared_for_training: bool
    notes: Optional[str]
    evaluated_by_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
