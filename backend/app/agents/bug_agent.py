from backend.app.models.bug_report import BugReport

from backend.app.rules.bug.division_by_zero import DivisionByZeroRule
from backend.app.rules.bug.infinite_recursion_rule import InfiniteRecursionRule
from backend.app.rules.bug.unreachable_code_rule import UnreachableCodeRule


class BugAgent:

    def __init__(self):

        self.rules = [
            DivisionByZeroRule(),
            InfiniteRecursionRule(),
            UnreachableCodeRule(),
        ]

    def find_bugs(self, parser_result):

        findings = []

        for rule in self.rules:
            findings.extend(rule.check(parser_result))

        return BugReport(
            has_bugs=len(findings) > 0,
            bug_count=len(findings),
            findings=findings
        )