import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class InfiniteRecursionRule(BaseRule):

    def check(self, parser_result):

        findings = []

        tree = parser_result.ast

        if tree is None:
            return findings

        for node in ast.walk(tree):

            if not isinstance(node, ast.FunctionDef):
                continue

            function_name = node.name

            for child in ast.walk(node):

                if (
                    isinstance(child, ast.Call)
                    and isinstance(child.func, ast.Name)
                    and child.func.id == function_name
                ):

                    findings.append(
                        Finding(
                            agent="BugAgent",
                            category="Bug",
                            severity="High",
                            title="Infinite Recursion",
                            explanation=f"Function '{function_name}' calls itself without an obvious terminating condition.",
                            recommendation="Add a base case before making the recursive call."
                        )
                    )

                    # Prevent duplicate findings for the same function
                    break

        return findings