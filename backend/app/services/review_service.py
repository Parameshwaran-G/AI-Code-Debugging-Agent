from backend.app.agents.parser_agent import ParserAgent
from backend.app.agents.bug_agent import BugAgent
from backend.app.agents.llm_agent import LLMAgent


class ReviewService:

    def __init__(self):
        self.parser = ParserAgent()
        self.bug_agent = BugAgent()
        self.llm = LLMAgent()

    def review(self, code: str):

        parser_result = self.parser.parse(code)

        bug_report = self.bug_agent.find_bugs(parser_result)

        llm_result = self.llm.explain(parser_result, bug_report)

        return {
            "parser": parser_result,
            "bugs": bug_report,
            "ai_review": llm_result
        }