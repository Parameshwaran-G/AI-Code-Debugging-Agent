import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class HardcodedPasswordRule(BaseRule):

    RULE_ID = "SEC001"
    TITLE = "Hardcoded Password"
    CATEGORY = "Security"
    SEVERITY = "High"
    TAGS = ["security", "credentials"]

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
                            rule_id=self.RULE_ID,
                            agent="SecurityAgent",
                            category=self.CATEGORY,
                            severity=self.SEVERITY,
                            title=self.TITLE,
                            explanation="Credentials are embedded directly in the source code.",
                            recommendation="Store credentials in environment variables or a secrets manager.",
                            line=node.lineno,
                            column=node.col_offset,
                            confidence=100,
                            tags=self.TAGS,
                        )
                    )

        return findings