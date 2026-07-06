from backend.app.models.bug_report import BugReport
from backend.app.models.finding import Finding


class BugAgent:

    def find_bugs(self, parser_result):

        code = parser_result.code

        findings = []

        # Division by zero
        if "/ 0" in code or "/0" in code:

            findings.append(
                Finding(
                    agent="BugAgent",
                    category="Bug",
                    severity="High",
                    title="Division by Zero",
                    explanation="The code performs integer division using zero as the divisor. In Java, this throws an ArithmeticException at runtime.",
                    recommendation="Validate the divisor before performing the division."
                )
            )

        return BugReport(
            has_bugs=len(findings) > 0,
            bug_count=len(findings),
            findings=findings
        )