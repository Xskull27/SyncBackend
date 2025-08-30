# from typing import List, Optional
# from uuid import UUID
# from datetime import datetime
# from pydantic import EmailStr, Field
# from app.schemas.base import Base

# #base
# class UserBase(Base):
#     email: EmailStr
#     username: str
#     role: str = Field(..., regex="^(PM|Developer|Designer)$")

# #user creation
# class NewUserInput(UserBase):
#     password: str

# #user read 
# class UserOutput(UserBase):
#     id: UUID
#     username:str
#     created_at: datetime
#     updated_at: datetime


# # class UserIssueRead(Base):
# #     id: UUID
# #     title: str


# # class ProjectRead(Base):
# #     id: UUID
# #     name: str


# class UserReadWithRelations(UserRead):
#     projects: List[ProjectRead] = []
#     assigned_issues: List[IssueRead] = []
#     created_issues: List[IssueRead] = []


