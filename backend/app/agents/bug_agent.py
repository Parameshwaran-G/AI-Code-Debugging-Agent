import ast

from backend.app.models.bug_report import BugReport
from backend.app.models.finding import Finding


class BugAgent:

    def find_bugs(self, parser_result):

        findings = []

        tree = parser_result.ast

        if tree is None:
            return BugReport(
                has_bugs=False,
                bug_count=0,
                findings=[]
            )

        # -----------------------------
        # Division by Zero
        # -----------------------------
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
                        recommendation="Validate the divisor before division."
                    )
                )

        # -----------------------------
        # Infinite Recursion
        # -----------------------------
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
                                agent="BugAgent",
                                category="Bug",
                                severity="High",
                                title="Infinite Recursion",
                                explanation=f"Function '{function_name}' calls itself without an obvious terminating condition.",
                                recommendation="Add a base case before making the recursive call."
                            )
                        )

                        break

        return BugReport(
            has_bugs=len(findings) > 0,
            bug_count=len(findings),
            findings=findings
        )