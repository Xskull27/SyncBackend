from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from project_sync_backend.app.db.database import get_session
from project_sync_backend.app.models.projects import Project
from project_sync_backend.app.models.issue import Issue, IssueStatus, IssuePriority

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats(session: Session = Depends(get_session)):
    total_projects = session.query(Project).count()
    total_issues = session.query(Issue).count()
    open_issues = session.query(Issue).filter(Issue.status == IssueStatus.OPEN).count()
    completed_issues = session.query(Issue).filter(Issue.status == IssueStatus.COMPLETED).count()
    high_priority_issues = session.query(Issue).filter(Issue.priority == IssuePriority.HIGH).count()
    recent_issues = session.query(Issue).order_by(desc(Issue.created_at)).limit(5).all()
    recent_projects = session.query(Project).order_by(desc(Project.created_at)).limit(5).all()

    def issue_to_dict(issue):
        return {
            "id": issue.id,
            "title": getattr(issue, "title", None),
            "status": getattr(issue, "status", None),
            "priority": getattr(issue, "priority", None),
            "created_at": getattr(issue, "created_at", None)
        }

    def project_to_dict(project):
        return {
            "id": project.id,
            "name": getattr(project, "name", None),
            "created_at": getattr(project, "created_at", None)
        }

    return {
        "totalProjects": total_projects,
        "totalIssues": total_issues,
        "openIssues": open_issues,
        "completedIssues": completed_issues,
        "highPriorityIssues": high_priority_issues,
        "recentIssues": [issue_to_dict(i) for i in recent_issues],
        "recentProjects": [project_to_dict(p) for p in recent_projects]
    }
