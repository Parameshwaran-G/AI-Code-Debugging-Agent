from pydantic import BaseModel


class LLMReview(BaseModel):
    summary: str
    severity: str
    explanation: str
    fix: str
    best_practice: str