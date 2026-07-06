from typing import Any

from pydantic import BaseModel


class ParserResult(BaseModel):
    code: str
    language: str
    syntax_valid: bool
    errors: list[str]
    ast: Any | None = None