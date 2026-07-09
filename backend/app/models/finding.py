from pydantic import BaseModel


class Finding(BaseModel):
    rule_id: str

    agent: str
    category: str
    severity: str

    title: str
    explanation: str
    recommendation: str

    line: int | None = None
    column: int | None = None

    confidence: int = 100
    tags: list[str] = []