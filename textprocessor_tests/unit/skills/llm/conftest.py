# import required modules
import pytest
from textprocessor.skills.llm import get_nlp, get_results
from collections import namedtuple

# import fixtures
from textprocessor_tests.test_utils.fixtures import conn, get_skill_data, verify_result, test


@pytest.fixture
def verify_detection():
    yield _verify_detection

def _verify_detection(doc, *args):
    expected_results = [{
        "comp_index": result.comp_index,
        "start": result.start,
        "end": result.end,
        "flag": result.flag
    } for result in args if result]

    print(f"\nExpect: {expected_results}")
    print(f"Get: {get_results(doc)}\n")

    assert get_results(doc) == expected_results


# Detect components with LLM test case factory
@pytest.fixture
def detect_with_llm(create_doc, get_skill_data, verify_result):
    def _detect_with_llm(test):
        metadata = get_skill_data(test.context['skill_id'])
        
        
        verify_result(
            test.context,
            *test.result,
        )

    return _detect_with_llm
