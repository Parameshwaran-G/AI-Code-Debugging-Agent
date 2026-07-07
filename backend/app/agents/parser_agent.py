import ast

from backend.app.models.parser_result import ParserResult


class ParserAgent:

    def parse(self, code: str) -> ParserResult:

        language = self.detect_language(code)

        syntax_valid = True
        errors = []
        tree = None

        if language == "python":

            try:
                tree = ast.parse(code)

            except SyntaxError as e:
                syntax_valid = False
                errors.append(str(e))

        return ParserResult(
            code=code,
            language=language,
            syntax_valid=syntax_valid,
            errors=errors,
            ast=tree
        )

    def detect_language(self, code: str):

        if "public class" in code:
            return "java"

        if "#include" in code:
            return "cpp"

        if "def " in code:
            return "python"

        return "unknown"