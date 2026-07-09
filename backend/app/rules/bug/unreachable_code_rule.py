import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class UnreachableCodeRule(BaseRule):

    RULE_ID = "BUG003"
    TITLE = "Unreachable Code"
    CATEGORY = "Bug"
    SEVERITY = "Medium"
    TAGS = ["bug", "control-flow"]

    def check(self, parser_result):

        findings = []

        tree = parser_result.ast

        if tree is None:
            return findings

        for node in ast.walk(tree):

            if not isinstance(node, ast.FunctionDef):
                continue

            unreachable = False

            for statement in node.body:

                if unreachable:

                    findings.append(
                        Finding(
                            rule_id=self.RULE_ID,
                            agent="BugAgent",
                            category=self.CATEGORY,
                            severity=self.SEVERITY,
                            title=self.TITLE,
                            explanation=(
                                "This statement can never be executed because "
                                "a previous statement exits the function."
                            ),
                            recommendation=(
                                "Remove the unreachable statement or move it "
                                "before the return or raise statement."
                            ),
                            line=statement.lineno,
                            column=statement.col_offset,
                            confidence=100,
                            tags=self.TAGS,
                        )
                    )

                if isinstance(statement, (ast.Return, ast.Raise)):
                    unreachable = True

        return findings