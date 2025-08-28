from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.db.database import get_session
from app.models.projects import Project, ProjectCreate, ProjectResponse, ProjectWithIssues
from app.models.issue import Issue
from app.models.user import User
from app.api.dependencies import get_current_user, get_current_pm

router = APIRouter()

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_pm)
):
    db_project = Project(
        title=project.title,
        description=project.description,
        pm_id=current_user.id
    )
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.get("/", response_model=List[ProjectWithIssues])
def get_projects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Project).where(Project.is_active == True)
    projects = session.exec(statement).all()
    
    result = []
    for project in projects:
        # Get project manager info
        pm_statement = select(User).where(User.id == project.pm_id)
        pm = session.exec(pm_statement).first()
        
        # Get issues count
        issues_statement = select(Issue).where(Issue.project_id == project.id)
        issues = session.exec(issues_statement).all()
        
        project_data = ProjectWithIssues(
            **project.model_dump(),
            issues_count=len(issues),
            open_issues=len([i for i in issues if i.status in ["OPEN", "ASSIGNED", "IN_PROGRESS", "REVIEW"]]),
            completed_issues=len([i for i in issues if i.status == "COMPLETED"]),
            project_manager_name=pm.username if pm else "Unknown"
        )
        result.append(project_data)
    
    return result

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Project).where(Project.id == project_id)
    project = session.exec(statement).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str,
    project_update: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_pm)
):
    statement = select(Project).where(Project.id == project_id)
    project = session.exec(statement).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Only PM who created the project can update it
    if project.pm_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update projects you created"
        )
    
    project.title = project_update.title
    project.description = project_update.description
    project.updated_at = datetime.utcnow()
    
    session.commit()
    session.refresh(project)
    return project