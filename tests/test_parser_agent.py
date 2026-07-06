from backend.app.agents.parser_agent import ParserAgent


def test_detect_java():

    parser = ParserAgent()

    result = parser.parse(
        "public class Test { }"
    )

    assert result.language == "java"