# import required modules
import pytest

# import fixtures
from textprocessor_tests.test_utils.fixtures import conn, get_skill_data, verify_result, test

# markup util function test case factory
@pytest.fixture
def markup_tcf(verify_result):
    def _markup_tcf(test, transformer=None, *transformerArgs):
        result = test.test_func(test.context['text'], test.context['llm_markup'])
        
        verify_result(test.context, test.expected_result, result, transformer, *transformerArgs)

    return _markup_tcf