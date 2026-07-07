import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class DivisionByZeroRule(BaseRule):

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
                        agent="BugAgent",
                        category="Bug",
                        severity="High",
                        title="Division by Zero",
                        explanation="The code performs division using zero.",
                        recommendation="Validate the divisor before performing division."
                    )
                )

        return findings