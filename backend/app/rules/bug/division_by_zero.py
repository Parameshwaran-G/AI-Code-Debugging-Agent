import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class DivisionByZeroRule(BaseRule):

    RULE_ID = "BUG001"
    TITLE = "Division by Zero"
    CATEGORY = "Bug"
    SEVERITY = "High"
    TAGS = ["bug", "arithmetic"]

    def check(self, parser_result):

        findings = []

        tree = parser_result.ast

        if tree is None:
            return findings

        for node in ast.walk(tree):

            if (
                isinstance(node, ast.BinOp)
                and isinstance(node.op, ast.Div)
                and isinstance(node.right, ast.Constant)
                and node.right.value == 0
            ):

                findings.append(
                    Finding(
                        rule_id=self.RULE_ID,
                        agent="BugAgent",
                        category=self.CATEGORY,
                        severity=self.SEVERITY,
                        title=self.TITLE,
                        explanation="The code performs division using zero.",
                        recommendation="Validate the divisor before division.",
                        line=node.lineno,
                        column=node.col_offset,
                        confidence=100,
                        tags=self.TAGS,
                    )
                )

        return findings