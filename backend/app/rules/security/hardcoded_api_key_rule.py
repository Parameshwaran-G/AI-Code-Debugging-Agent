import ast

from backend.app.models.finding import Finding
from backend.app.rules.base_rule import BaseRule


class HardcodedApiKeyRule(BaseRule):

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
                    and target.id.lower() in ["apikey", "api_key"]
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                ):

                    findings.append(
                        Finding(
                            agent="SecurityAgent",
                            category="Security",
                            severity="High",
                            title="Hardcoded API Key",
                            explanation="API keys should never be stored directly in source code.",
                            recommendation="Move API keys to environment variables."
                        )
                    )

        return findings