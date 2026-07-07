import ast

from backend.app.models.finding import Finding
from backend.app.models.security_report import SecurityReport


class SecurityAgent:

    def scan(self, parser_result):

        findings = []

        tree = parser_result.ast

        if tree is None:
            return SecurityReport(
                has_security_issues=False,
                issue_count=0,
                findings=[]
            )

        for node in ast.walk(tree):

            # ----------------------------------------
            # Hardcoded Password / API Key / Secret
            # ----------------------------------------
            if isinstance(node, ast.Assign):

                for target in node.targets:

                    if not isinstance(target, ast.Name):
                        continue

                    variable = target.id.lower()

                    if (
                        isinstance(node.value, ast.Constant)
                        and isinstance(node.value.value, str)
                    ):

                        if "password" in variable:

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

                        elif "api_key" in variable or "apikey" in variable:

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

                        elif "secret" in variable:

                            findings.append(
                                Finding(
                                    agent="SecurityAgent",
                                    category="Security",
                                    severity="High",
                                    title="Hardcoded Secret",
                                    explanation="Secrets should not be embedded directly in source code.",
                                    recommendation="Use a secure secret manager."
                                )
                            )

            # ----------------------------------------
            # Dangerous eval()
            # ----------------------------------------
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

        return SecurityReport(
            has_security_issues=len(findings) > 0,
            issue_count=len(findings),
            findings=findings
        )