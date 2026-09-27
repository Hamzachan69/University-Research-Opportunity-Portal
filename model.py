# ==============================================================================
# IMPORTS
# ==============================================================================

# BaseModel is the foundation for creating data models (schemas) in Pydantic.
# It provides automatic data validation, type conversion, and JSON serialization.
# Field allows us to define extra validation rules (like minimum length, greater than, etc.)
# and attach metadata or default values to model attributes.
from pydantic import BaseModel, Field

# date provides a Python date object (year, month, day).
# When used as a type annotation in Pydantic, it automatically converts incoming
# ISO format date strings (e.g., "2026-10-15") into Python datetime.date objects.
from datetime import date

# Enum is Python's standard library class for creating enumerations (fixed set of constants).
from enum import Enum

# Optional is used for type hinting when a value can either be of a specific type or None.
# For example, Optional[str] means the value can be a string OR None.
from typing import Optional


# ==============================================================================
# ENUMERATIONS
# ==============================================================================

# Inheriting from both 'str' and 'Enum' creates a string-based enum.
# Why 'str'? This ensures the values serialize directly to JSON strings and are
# compatible with database VARCHAR/ENUM columns without needing custom serializers.
class StatusEnum(str, Enum):
    # Represents an opportunity that is currently accepting applications.
    open = "Open"
    # Represents an opportunity that has expired or is no longer accepting applications.
    closed = "Closed"


# ==============================================================================
# SCHEMAS / MODELS
# ==============================================================================

# ------------------------------------------------------------------------------
# OpportunityCreate Schema
# ------------------------------------------------------------------------------
# Used when creating a NEW research opportunity (e.g., via a POST request).
# Every field required to create a complete database record is defined here.
class OpportunityCreate(BaseModel):
    # Title of the research project.
    # '...' (Ellipsis) specifies that this field is MANDATORY (required).
    # 'min_length=1' prevents empty strings ("") from being accepted.
    title: str = Field(..., min_length=1)

    # Detailed description of what the research project entails.
    # Mandatory and cannot be empty.
    description: str = Field(..., min_length=1)

    # The field or domain of research (e.g., "Artificial Intelligence", "Bioinformatics").
    # Required string.
    research_area: str

    # The name of the professor or researcher supervising this opportunity.
    # Required string.
    faculty_name: str

    # The academic department offering the opportunity (e.g., "Computer Science").
    # Required string.
    department: str

    # The prerequisites or skills needed from applying students (e.g., "Python, PyTorch").
    # Required string.
    required_skills: str

    # Number of student openings available for this project.
    # '...' means it is mandatory.
    # 'gt=0' (greater than 0) ensures only positive whole numbers (1, 2, 3...) are allowed.
    available_positions: int = Field(..., gt=0)

    # Cut-off deadline for student applications.
    # Automatically validates and parses "YYYY-MM-DD" date strings.
    application_deadline: date

    # Current status of the opportunity.
    # Defaults to StatusEnum.open ("Open") so callers do not need to pass it explicitly on creation.
    status: StatusEnum = StatusEnum.open


# ------------------------------------------------------------------------------
# OpportunityUpdate Schema
# ------------------------------------------------------------------------------
# Used when UPDATING an existing opportunity (e.g., via a PATCH or partial PUT request).
# Notice that every field is marked Optional[...] with a default value of None.
# Why? Because in an update request, the user may only want to modify one or two fields
# (e.g., updating only the status or available_positions) without re-sending the whole object.
# Fields left as None will be ignored during the update.
class OpportunityUpdate(BaseModel):
    # Optional new title; if not provided, defaults to None (no change).
    title: Optional[str] = None

    # Optional new description.
    description: Optional[str] = None

    # Optional new research domain.
    research_area: Optional[str] = None

    # Optional new supervising faculty name.
    faculty_name: Optional[str] = None

    # Optional new academic department.
    department: Optional[str] = None

    # Optional new required skill set.
    required_skills: Optional[str] = None

    # Optional new number of positions.
    available_positions: Optional[int] = None

    # Optional new application deadline.
    application_deadline: Optional[date] = None

    # Optional new status ("Open" or "Closed").
    status: Optional[StatusEnum] = None
