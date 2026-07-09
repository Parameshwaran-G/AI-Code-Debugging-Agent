import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class InfiniteRecursionRule(BaseRule):

    RULE_ID = "BUG002"
    TITLE = "Infinite Recursion"
    CATEGORY = "Bug"
    SEVERITY = "High"
    TAGS = ["bug", "recursion"]

    def check(self, parser_result):

        findings = []

        tree = parser_result.ast

        if tree is None:
            return findings

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                function_name = node.name

                for child in ast.walk(node):

                    if (
                        isinstance(child, ast.Call)
                        and isinstance(child.func, ast.Name)
                        and child.func.id == function_name
                    ):

                        findings.append(
                            Finding(
                                rule_id=self.RULE_ID,
                                agent="BugAgent",
                                category=self.CATEGORY,
                                severity=self.SEVERITY,
                                title=self.TITLE,
                                explanation=(
                                    f"Function '{function_name}' calls itself "
                                    "without an obvious terminating condition."
                                ),
                                recommendation="Add a base case before making the recursive call.",
                                line=child.lineno,
                                column=child.col_offset,
                                confidence=100,
                                tags=self.TAGS,
                            )
                        )

                        break

        return findings