from typing import Any

from pydantic import BaseModel, Field


class ParserResult(BaseModel):
    code: str
    language: str
    syntax_valid: bool
    errors: list[str]

    # Internal AST used by analysis agents.
    # It is excluded from API responses because ast.Module
    # cannot be serialized to JSON.
    ast: Any | None = Field(default=None, exclude=True)