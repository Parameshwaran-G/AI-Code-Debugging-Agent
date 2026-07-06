import re

from backend.app.models.finding import Finding
from backend.app.models.security_report import SecurityReport


class SecurityAgent:

    def scan(self, parser_result):

        code = parser_result.code

        findings = []

        if re.search(r'password\s*=\s*["\'].*?["\']', code, re.IGNORECASE):

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

        if re.search(r'api[_-]?key\s*=\s*["\'].*?["\']', code, re.IGNORECASE):

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

        if "SELECT" in code.upper() and "+" in code:

            findings.append(
                Finding(
                    agent="SecurityAgent",
                    category="Security",
                    severity="High",
                    title="Possible SQL Injection",
                    explanation="Building SQL queries using string concatenation may allow SQL Injection.",
                    recommendation="Use parameterized queries or prepared statements."
                )
            )

        if "eval(" in code:

            findings.append(
                Finding(
                    agent="SecurityAgent",
                    category="Security",
                    severity="Medium",
                    title="Dangerous use of eval()",
                    explanation="eval() executes arbitrary code and can be dangerous.",
                    recommendation="Avoid eval() on untrusted input."
                )
            )

        return SecurityReport(
            has_security_issues=len(findings) > 0,
            issue_count=len(findings),
            findings=findings
        )