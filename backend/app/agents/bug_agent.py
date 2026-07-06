from backend.app.models.parser_result import ParserResult
from backend.app.models.bug_report import BugReport


class BugAgent:

    def find_bugs(self, parser_result: ParserResult) -> BugReport:

        bugs = []

        code = parser_result.code

        # Rule 1: Division by zero
        if "/0" in code or "/ 0" in code:
            bugs.append("Possible division by zero.")

        return BugReport(
            has_bugs=len(bugs) > 0,
            bug_count=len(bugs),
            bugs=bugs
        )