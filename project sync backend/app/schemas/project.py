from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.schemas.base import Base

# Base fields shared across project schemas
class ProjectBase(Base):
    name: str
    description: Optional[str] = None

# For creating a new project
class ProjectCreateInput(ProjectBase):
    pm_id: UUID#

# For reading project details
class ProjectRead(ProjectBase):
    id: UUID
    pm_id: UUID
    created_at: datetime
    updated_at: datetime

# For updating a project
class ProjectUpdate(Base):
    name: Optional[str] = None
    description: Optional[str] = None