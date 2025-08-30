# # Import models here for convenient access
# # Use local imports inside functions or type checking to avoid circular imports if needed

# from .user import User
# from .projects import Project
# from .issue import Issue

# __all__ = ["User", "Project", "Issue"]


from .user import User, UserCreate, UserResponse, UserLogin, Token, TokenData, UserRole
from .projects import Project, ProjectCreate, ProjectResponse, ProjectWithIssues
from .issue import Issue, IssueCreate, IssueResponse, IssueAssign, IssueStatusUpdate, IssueWithDetails, IssueStatus, IssuePriority, IssueType

__all__ = [
    "User", "UserCreate", "UserResponse", "UserLogin", "Token", "TokenData", "UserRole",
    "Project", "ProjectCreate", "ProjectResponse", "ProjectWithIssues",
    "Issue", "IssueCreate", "IssueResponse", "IssueAssign", "IssueStatusUpdate", 
    "IssueWithDetails", "IssueStatus", "IssuePriority", "IssueType"
]