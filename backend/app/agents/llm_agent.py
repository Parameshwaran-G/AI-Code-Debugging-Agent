import requests


class LLMAgent:

    def __init__(self, model: str = "qwen2.5:3b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def explain(self, parser_result, bug_report):

        prompt = self.build_prompt(parser_result, bug_report)

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()

        return {
            "summary": data.get("response", "")
        }

    def build_prompt(self, parser_result, bug_report):

        return f"""
You are a senior software engineer reviewing code.

Language: {parser_result.language}

Code:
{parser_result.code}

Bug Report:
{bug_report.bugs}

Explain:
1. What is wrong
2. Why it is a problem
3. How to fix it
"""