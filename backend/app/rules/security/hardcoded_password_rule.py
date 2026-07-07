import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class HardcodedPasswordRule(BaseRule):

    def check(self, parser_result):

        findings = []

        tree = parser_result.ast

        if tree is None:
            return findings

        for node in ast.walk(tree):

            if not isinstance(node, ast.Assign):
                continue

            for target in node.targets:

                if (
                    isinstance(target, ast.Name)
                    and "password" in target.id.lower()
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                ):

                    findings.append(
                        Finding(
                            agent="SecurityAgent",
                            category="Security",
                            severity="High",
                            title="Hardcoded Password",
                            explanation="Credentials are embedded directly in the source code.",
                            recommendation="Store credentials in environment variables or a secrets manager."
                        )
                    )

        return findings