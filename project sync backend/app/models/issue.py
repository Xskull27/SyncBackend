from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class IssueStatus(str, Enum):
    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    COMPLETED = "COMPLETED"

class IssuePriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IssueType(str, Enum):
    BUG = "BUG"
    TASK = "TASK"
    FEATURE = "FEATURE"
    ENHANCEMENT = "ENHANCEMENT"

class IssueBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = None
    priority: IssuePriority
    issue_type: IssueType

class Issue(IssueBase, table=True):
    __tablename__ = "issues"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    status: IssueStatus = Field(default=IssueStatus.OPEN)
    project_id: UUID = Field(foreign_key="projects.id")
    assigned_to_id: Optional[UUID] = Field(foreign_key="users.id", default=None)
    created_by_id: UUID = Field(foreign_key="users.id")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationships
    project: Optional["Project"] = Relationship(back_populates="issues")
    assignee: Optional["User"] = Relationship(
        back_populates="assigned_issues",
        sa_relationship_kwargs={"foreign_keys": "Issue.assigned_to_id"}
    )
    creator: Optional["User"] = Relationship(
        back_populates="created_issues",
        sa_relationship_kwargs={"foreign_keys": "Issue.created_by_id"}
    )

class IssueCreate(IssueBase):
    project_id: UUID

class IssueResponse(IssueBase):
    id: UUID
    status: IssueStatus
    project_id: UUID
    assigned_to_id: Optional[UUID] = None
    created_by_id: UUID
    created_at: datetime

class IssueAssign(SQLModel):
    assigned_to_id: UUID

class IssueStatusUpdate(SQLModel):
    status: IssueStatus

class IssueWithDetails(IssueResponse):
    project_title: str
    assignee_name: Optional[str] = None
    creator_name: str