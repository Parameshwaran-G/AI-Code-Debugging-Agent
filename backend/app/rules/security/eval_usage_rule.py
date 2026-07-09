import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class EvalUsageRule(BaseRule):

    RULE_ID = "SEC003"
    TITLE = "Dangerous use of eval()"
    CATEGORY = "Security"
    SEVERITY = "Medium"
    TAGS = ["security", "code-injection"]

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
                        rule_id=self.RULE_ID,
                        agent="SecurityAgent",
                        category=self.CATEGORY,
                        severity=self.SEVERITY,
                        title=self.TITLE,
                        explanation="eval() executes arbitrary Python code and can lead to code injection.",
                        recommendation="Avoid eval() on untrusted input.",
                        line=node.lineno,
                        column=node.col_offset,
                        confidence=100,
                        tags=self.TAGS,
                    )
                )

        return findings