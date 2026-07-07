import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class EvalUsageRule(BaseRule):

    def check(self, parser_result):

        findings = []

        tree = parser_result.ast

        if tree is None:
            return findings

        for node in ast.walk(tree):

            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "eval"
            ):

                findings.append(
                    Finding(
                        agent="SecurityAgent",
                        category="Security",
                        severity="Medium",
                        title="Dangerous use of eval()",
                        explanation="eval() executes arbitrary Python code and can lead to code injection.",
                        recommendation="Avoid eval() on untrusted input."
                    )
                )

        return findings