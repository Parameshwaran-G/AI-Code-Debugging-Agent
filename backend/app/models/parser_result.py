from typing import Any

from pydantic import BaseModel


class ParserResult(BaseModel):
    code: str
    language: str
    syntax_valid: bool
    errors: list[str]

    # Internal object used by other agents.
    # Excluded from API responses.
    ast: Any | None = None

    model_config = {
        "arbitrary_types_allowed": True
    }