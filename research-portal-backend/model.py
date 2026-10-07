from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from typing import Optional

class StatusEnum(str, Enum):
    open = "Open"
    closed = "Closed"

class OpportunityCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    research_area: str
    faculty_name: str
    department: str
    required_skills: str
    available_positions: int = Field(..., gt=0)
    application_deadline: date
    status: StatusEnum = StatusEnum.open

class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    research_area: Optional[str] = None
    faculty_name: Optional[str] = None
    department: Optional[str] = None
    required_skills: Optional[str] = None
    available_positions: Optional[int] = None
    application_deadline: Optional[date] = None
    status: Optional[StatusEnum] = None