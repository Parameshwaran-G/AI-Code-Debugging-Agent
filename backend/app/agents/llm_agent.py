import json
import requests

from backend.app.models.llm_review import LLMReview


class LLMAgent:

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:3b"

    def explain(self, parser_result, bug_report, security_report):

        findings = bug_report.findings + security_report.findings

        if not findings:
            return LLMReview(
                summary="No issues detected.",
                severity="None",
                explanation=(
                    "ParserAgent, BugAgent and SecurityAgent did not detect any issues."
                ),
                fix="No changes are required.",
                best_practice=(
                    "Continue following clean coding practices and write unit tests."
                )
            )

        severity_order = {
            "Low": 1,
            "Medium": 2,
            "High": 3
        }

        highest_severity = "Low"

        for finding in findings:
            if (
                severity_order.get(finding.severity, 0)
                > severity_order.get(highest_severity, 0)
            ):
                highest_severity = finding.severity

        findings_text = ""

        for index, finding in enumerate(findings, start=1):

            findings_text += f"""
Issue {index}

Rule ID: {finding.rule_id}
Title: {finding.title}
Category: {finding.category}
Severity: {finding.severity}

Location:
Line: {finding.line}
Column: {finding.column}

Confidence: {finding.confidence}%

Tags:
{", ".join(finding.tags)}

Explanation:
{finding.explanation}

Recommendation:
{finding.recommendation}

----------------------------------------
"""

        prompt = f"""
You are an expert Python static code analysis assistant.

The static analysis engine has already identified the issues.

Your task is ONLY to explain the reported findings.

Programming Language:
{parser_result.language}

Detected Findings:

{findings_text}

Source Code:

{parser_result.code}

STRICT RULES:

1. Explain ONLY the detected findings.
2. Do NOT detect additional bugs or security issues.
3. Do NOT rewrite the user's source code.
4. Do NOT invent variable names.
5. Do NOT provide fixes using the user's variables.
6. Give generic fixes that apply to similar code.
7. Keep the explanation concise and professional.
8. If multiple findings exist, summarize them together.

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

            print("\n========== RAW OLLAMA RESPONSE ==========")
            print(content)
            print("=========================================\n")

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

        except (
            requests.RequestException,
            json.JSONDecodeError,
            KeyError
        ) as e:

            return LLMReview(
                summary="LLM Error",
                severity=highest_severity,
                explanation=f"Failed to generate AI review: {str(e)}",
                fix="Verify Ollama is running and returning valid JSON.",
                best_practice=(
                    "Always validate responses received from external AI services."
                )
            )