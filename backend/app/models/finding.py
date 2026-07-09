from pydantic import BaseModel


class Finding(BaseModel):
    agent: str
    category: str
    severity: str
    title: str

    explanation: str
    recommendation: str

    line: int | None = None
    column: int | None = None