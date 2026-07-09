import ast

from backend.app.models.parser_result import ParserResult


class ParserAgent:

    def parse(self, code: str) -> ParserResult:

        syntax_valid = True
        errors = []
        tree = None

        try:
            tree = ast.parse(code)
            language = "python"

        except SyntaxError as e:
            syntax_valid = False
            errors.append(str(e))
            language = "python"

        return ParserResult(
            code=code,
            language=language,
            syntax_valid=syntax_valid,
            errors=errors,
            ast=tree
        )