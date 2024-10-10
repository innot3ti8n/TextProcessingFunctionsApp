# import required
from textprocessor.utils import get_results

# import functions / module contains functions to test
from textprocessor.handlers.llm import openai_gpt

# Test cases
def test_skill2_prompt_1(test, detect_with_llm):
    test(
        openai_gpt.process_text
    ).given({
        'text': "",
        'skill_id': 2
    }).expects(
        ''
    ).using(
        detect_with_llm
    )