from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from pydantic import EmailStr,validator,model_validator
from app.core.validators import validate_email, validate_password, validate_username,StripWhitespaceMixin

class UserRole(str, Enum):
    PM = "PM"
    DEVELOPER = "Developer"
    DESIGNER = "Designer"

class UserBase(StripWhitespaceMixin, SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    username: str = Field(index=True, max_length=100)
    role: UserRole
    is_active: bool = Field(default=True)

    @validator("username")
    def username_valid(cls, value): return validate_username(cls, value)

    @validator("email")
    def email_valid(cls, value): return validate_email(cls, value)

    
    

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    password_hash: str = Field(max_length=255)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Relationships
    managed_projects: List["Project"] = Relationship(back_populates="project_manager")
    created_issues: List["Issue"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "Issue.created_by_id"}
    )
    assigned_issues: List["Issue"] = Relationship(
        back_populates="assignee",
        sa_relationship_kwargs={"foreign_keys": "Issue.assigned_to_id"}
    )

class UserCreate(UserBase):
    password: str
    confirm_password: str 

    @validator("password")
    def password_valid(cls, value): return validate_password(cls, value)

    @model_validator(mode="after")
    def passwords_match(cls, values):
        if values.password != values.confirm_password:
            raise ValueError("Password and Confirm Password do not match.")
        return values

# class UserResponse(UserBase):
#     id: UUID
#     created_at: datetime

class UserResponse(SQLModel):
    id: UUID
    email: EmailStr
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime


class UserLogin(SQLModel):
    email: EmailStr
    password: str

    @validator("password")
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError("Password must not be empty.")
        return value

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    email: Optional[str] = None