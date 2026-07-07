from backend.app.models.security_report import SecurityReport

from backend.app.rules.security.hardcoded_password_rule import HardcodedPasswordRule
from backend.app.rules.security.hardcoded_api_key_rule import HardcodedApiKeyRule
from backend.app.rules.security.eval_usage_rule import EvalUsageRule


class SecurityAgent:

    def __init__(self):

        self.rules = [
            HardcodedPasswordRule(),
            HardcodedApiKeyRule(),
            EvalUsageRule()
        ]

    def scan(self, parser_result):

        findings = []

        for rule in self.rules:
            findings.extend(rule.check(parser_result))

        return SecurityReport(
            has_security_issues=len(findings) > 0,
            issue_count=len(findings),
            findings=findings
        )