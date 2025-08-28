from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime
from app.db.database import get_session
from app.models.issue import Issue, IssueStatus, IssueCreate, IssueResponse, IssueAssign, IssueStatusUpdate, IssueWithDetails
from app.models.user import User, UserRole
from app.models.projects import Project
from app.api.dependencies import get_current_user, get_current_pm

router = APIRouter()

@router.post("/", response_model=IssueResponse)
def create_issue(
    issue: IssueCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Verify project exists
    project_statement = select(Project).where(Project.id == issue.project_id)
    project = session.exec(project_statement).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_issue = Issue(
        title=issue.title,
        description=issue.description,
        priority=issue.priority,
        issue_type=issue.issue_type,
        project_id=issue.project_id,
        created_by_id=current_user.id,
        status=IssueStatus.OPEN  # Always starts as OPEN
    )
    session.add(db_issue)
    session.commit()
    session.refresh(db_issue)
    return db_issue

@router.get("/", response_model=List[IssueWithDetails])
def get_issues(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == UserRole.PM:
        # PM can see all issues
        statement = select(Issue)
    else:
        # Others see only their assigned issues
        statement = select(Issue).where(Issue.assigned_to_id == current_user.id)
    
    issues = session.exec(statement).all()
    
    result = []
    for issue in issues:
        # Get project info
        project_statement = select(Project).where(Project.id == issue.project_id)
        project = session.exec(project_statement).first()
        
        # Get assignee info
        assignee = None
        if issue.assigned_to_id:
            assignee_statement = select(User).where(User.id == issue.assigned_to_id)
            assignee = session.exec(assignee_statement).first()
        
        # Get creator info
        creator_statement = select(User).where(User.id == issue.created_by_id)
        creator = session.exec(creator_statement).first()
        
        issue_detail = IssueWithDetails(
            **issue.model_dump(),
            project_title=project.title if project else "Unknown",
            assignee_name=assignee.username if assignee else None,
            creator_name=creator.username if creator else "Unknown"
        )
        result.append(issue_detail)
    
    return result

@router.put("/{issue_id}/assign", response_model=IssueResponse)
def assign_issue(
    issue_id: str,
    assignment: IssueAssign,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_pm)
):
    # Get issue
    issue_statement = select(Issue).where(Issue.id == issue_id)
    issue = session.exec(issue_statement).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Verify assignee exists
    assignee_statement = select(User).where(User.id == assignment.assigned_to_id)
    assignee = session.exec(assignee_statement).first()
    if not assignee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    issue.assigned_to_id = assignment.assigned_to_id
    issue.status = IssueStatus.ASSIGNED
    issue.updated_at = datetime.utcnow()
    
    session.commit()
    session.refresh(issue)
    return issue

@router.put("/{issue_id}/status", response_model=IssueResponse)
def update_issue_status(
    issue_id: str,
    status_update: IssueStatusUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    issue_statement = select(Issue).where(Issue.id == issue_id)
    issue = session.exec(issue_statement).first()
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Permission checks
    if current_user.role != UserRole.PM:
        # Non-PM users can only update their assigned issues
        if issue.assigned_to_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update issues assigned to you"
            )
        
        # Non-PM users cannot mark as COMPLETED
        if status_update.status == IssueStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Project Manager can mark issues as completed"
            )
        
        # Non-PM users cannot work on OPEN issues
        if issue.status == IssueStatus.OPEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This issue must be assigned by PM before you can work on it"
            )
    
    # Status transition validation for non-PM users
    if current_user.role != UserRole.PM:
        valid_transitions = {
            IssueStatus.ASSIGNED: [IssueStatus.IN_PROGRESS],
            IssueStatus.IN_PROGRESS: [IssueStatus.REVIEW, IssueStatus.ASSIGNED],
            IssueStatus.REVIEW: [IssueStatus.IN_PROGRESS],  # Can go back to in progress
        }
        
        if issue.status not in valid_transitions or status_update.status not in valid_transitions[issue.status]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status transition from {issue.status} to {status_update.status}"
            )
    
    issue.status = status_update.status
    issue.updated_at = datetime.utcnow()
    
    session.commit()
    session.refresh(issue)
    return issue


@router.get("/my-issues", response_model=List[IssueWithDetails])
def get_my_issues(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Issue).where(Issue.created_by_id == current_user.id)
    issues = session.exec(statement).all()
    
    result = []
    for issue in issues:
        # Get project info
        project = session.exec(
            select(Project).where(Project.id == issue.project_id)
        ).first()
        
        # Get assignee info (if assigned)
        assignee_name = None
        if issue.assigned_to_id:
            assignee = session.exec(
                select(User).where(User.id == issue.assigned_to_id)
            ).first()
            assignee_name = assignee.username if assignee else None

        # Get creator info
        creator = session.exec(
            select(User).where(User.id == issue.created_by_id)
        ).first()
        
        issue_detail = IssueWithDetails(
            **issue.model_dump(),
            project_title=project.title if project else "Unknown",
            assignee_name=assignee_name,
            creator_name=creator.username if creator else "Unknown"
        )
        result.append(issue_detail)
    
    return result


@router.get("/open-issues", response_model=List[IssueWithDetails])
def get_open_issues(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_pm)
):
    """Get all open (unassigned) issues - PM only"""
    statement = select(Issue).where(Issue.status == IssueStatus.OPEN)
    issues = session.exec(statement).all()
    
    result = []
    for issue in issues:
        # Get project info
        project_statement = select(Project).where(Project.id == issue.project_id)
        project = session.exec(project_statement).first()
        
        # Get creator info
        creator_statement = select(User).where(User.id == issue.created_by_id)
        creator = session.exec(creator_statement).first()
        
        issue_detail = IssueWithDetails(
            **issue.model_dump(),
            project_title=project.title if project else "Unknown",
            assignee_name=None,
            creator_name=creator.username if creator else "Unknown"
        )
        result.append(issue_detail)
    
    return result