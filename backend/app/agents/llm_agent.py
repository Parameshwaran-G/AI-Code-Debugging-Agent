import json
import requests

from backend.app.models.llm_review import LLMReview


class LLMAgent:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:3b"

    def explain(self, parser_result, bug_report, security_report):

        # Collect all findings
        findings = bug_report.findings + security_report.findings

        # No findings -> No LLM call needed
        if not findings:
            return LLMReview(
                summary="No issues detected.",
                severity="None",
                explanation="ParserAgent, BugAgent and SecurityAgent did not detect any issues.",
                fix="No changes are required.",
                best_practice="Continue following clean coding practices and write unit tests."
            )

        # Determine highest severity from rule engine
        severity_order = {
            "Low": 1,
            "Medium": 2,
            "High": 3
        }

        highest_severity = "Low"

        for finding in findings:
            if severity_order.get(finding.severity, 0) > severity_order.get(highest_severity, 0):
                highest_severity = finding.severity

        findings_text = "\n".join(
            f"- {finding.title}" for finding in findings
        )

        prompt = f"""
You are a senior software engineer.

The analysis agents have already completed the review.

Programming Language:
{parser_result.language}

Detected Findings:
{findings_text}

Source Code:
{parser_result.code}

IMPORTANT:

- Explain ONLY the detected findings.
- Do NOT detect new bugs.
- Do NOT invent security issues.
- Do NOT assign severity.
- Do NOT perform another code review.
- Keep the explanation concise.

Return ONLY valid JSON.

{{
    "summary": "...",
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

            defaults = {
                "summary": f"Detected {len(findings)} issue(s).",
                "explanation": "No explanation provided.",
                "fix": "No fix provided.",
                "best_practice": "Follow clean coding practices."
            }

            for key, value in defaults.items():
                if key not in review or not str(review[key]).strip():
                    review[key] = value

            return LLMReview(
                summary=review["summary"],
                severity=highest_severity,
                explanation=review["explanation"],
                fix=review["fix"],
                best_practice=review["best_practice"]
            )

        except (requests.RequestException, json.JSONDecodeError, KeyError) as e:

            return LLMReview(
                summary="LLM Error",
                severity=highest_severity,
                explanation=f"Failed to generate AI review: {str(e)}",
                fix="Verify Ollama is running and returning valid JSON.",
                best_practice="Always validate responses received from external AI services."
            )