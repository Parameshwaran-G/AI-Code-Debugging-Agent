from backend.app.agents.parser_agent import ParserAgent
from backend.app.agents.bug_agent import BugAgent
from backend.app.agents.security_agent import SecurityAgent
from backend.app.agents.llm_agent import LLMAgent


class ReviewService:

    def __init__(self):

        self.parser = ParserAgent()
        self.bug_agent = BugAgent()
        self.security_agent = SecurityAgent()
        self.llm = LLMAgent()

    def review(self, code: str):

        # Step 1: Parse the source code
        parser_result = self.parser.parse(code)

        print("\n========== PARSER RESULT ==========")
        print(parser_result.model_dump())
        print("===================================\n")

        # Step 2: Detect bugs
        bug_report = self.bug_agent.find_bugs(parser_result)

        print("\n========== BUG REPORT ==========")
        print(bug_report.model_dump())
        print("================================\n")

        # Step 3: Detect security issues
        security_report = self.security_agent.scan(parser_result)

        print("\n========== SECURITY REPORT ==========")
        print(security_report.model_dump())
        print("====================================\n")

        # Step 4: Generate AI explanation
        ai_review = self.llm.explain(
            parser_result,
            bug_report,
            security_report
        )

        print("\n========== AI REVIEW ==========")
        print(ai_review.model_dump())
        print("================================\n")

        # Step 5: Return complete response
        return {
            "parser": parser_result,
            "bugs": bug_report,
            "security": security_report,
            "ai_review": ai_review
        }