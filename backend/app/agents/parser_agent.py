from backend.app.models.parser_result import ParserResult


class ParserAgent:

    def parse(self, code: str) -> ParserResult:

        language = self.detect_language(code)

        return ParserResult(
            code=code,
            language=language,
            syntax_valid=True,
            errors=[],
            ast=None
        )

    def detect_language(self, code: str):

        if "public class" in code:
            return "java"

        if "#include" in code:
            return "cpp"

        if "def " in code:
            return "python"

        return "unknown"