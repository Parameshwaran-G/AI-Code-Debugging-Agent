import json
import requests

from backend.app.models.llm_review import LLMReview


class LLMAgent:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:3b"

    def explain(self, parser_result, bug_report, security_report):

        # Collect findings from all worker agents
        findings = []

        if bug_report.has_bugs:
            findings.extend(
                finding.title
                for finding in bug_report.findings
            )

        if security_report.has_security_issues:
            findings.extend(
                finding.title
                for finding in security_report.findings
            )

        # No findings -> No need to call the LLM
        if not findings:
            return LLMReview(
                summary="No issues detected.",
                severity="None",
                explanation="ParserAgent, BugAgent and SecurityAgent did not detect any issues.",
                fix="No changes are required.",
                best_practice="Continue following clean coding practices and write unit tests."
            )

        prompt = f"""
You are a senior software engineer.

The analysis agents have already completed the review.

Programming Language:
{parser_result.language}

Detected Findings:
{chr(10).join("- " + item for item in findings)}

Source Code:
{parser_result.code}

IMPORTANT:

- Explain ONLY the detected findings.
- Do NOT detect new bugs.
- Do NOT invent security issues.
- Do NOT perform another code review.
- Keep the explanation concise.

Return ONLY valid JSON.

{{
    "summary": "...",
    "severity": "Low | Medium | High",
    "explanation": "...",
    "fix": "...",
    "best_practice": "..."
}}
"""

        try:

            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            response.raise_for_status()

            content = response.json()["response"].strip()

            review = json.loads(content)

            return LLMReview(**review)

        except Exception as e:

            return LLMReview(
                summary="LLM Error",
                severity="Unknown",
                explanation=str(e),
                fix="Verify Ollama is running and returning valid JSON.",
                best_practice="Always validate responses received from external AI services."
            )