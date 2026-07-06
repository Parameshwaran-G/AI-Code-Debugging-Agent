from pydantic import BaseModel


class BugReport(BaseModel):
    has_bugs: bool
    bug_count: int
    bugs: list[str]