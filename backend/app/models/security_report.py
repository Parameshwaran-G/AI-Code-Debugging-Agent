from pydantic import BaseModel
from backend.app.models.finding import Finding


class SecurityReport(BaseModel):
    has_security_issues: bool
    issue_count: int
    findings: list[Finding]