# from __future__ import annotations
# from typing import List, Optional
# from datetime import datetime
# from uuid import UUID, uuid4
# from sqlmodel import SQLModel, Field, Relationship

# class Project(SQLModel, table=True):
#     __tablename__ = "project"

#     id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
#     name: str = Field(nullable=False)
#     description: Optional[str] = Field(default=None)
#     pm_id: UUID = Field(nullable=False, foreign_key="user.id")
#     created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
#     updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

#     # Relationships
#     pm: Optional["User"] = Relationship(back_populates="projects")
#     issues: List["Issue"] = Relationship(back_populates="project")


from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class ProjectBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    is_active: bool = Field(default=True)

class Project(ProjectBase, table=True):
    __tablename__ = "projects"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    pm_id: UUID = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationships
    project_manager: Optional["User"] = Relationship(back_populates="managed_projects")
    issues: List["Issue"] = Relationship(back_populates="project")

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: UUID
    pm_id: UUID
    created_at: datetime

class ProjectWithIssues(ProjectResponse):
    issues_count: int
    open_issues: int
    completed_issues: int
    project_manager_name: str