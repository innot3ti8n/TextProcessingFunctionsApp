# import required modules
import pytest
from textprocessor.utils import get_results

# import fixtures
from textprocessor_tests.test_utils.fixtures import verify_result, test
from textprocessor_tests.test_utils.nlp_fixtures import nlp, create_doc

@pytest.fixture
def verify_detection(verify_result):
    def _verify_detection(context, doc, transformer, *transformerArgs, expected_results):
        # Print all tokens
        for token in doc:
            print(f'Token: {token.text}, POS: {token.pos_}, Lemma: {token.lemma_}, Ent: {token.ent_type_}')

        # Print all entities
        for ent in doc.ents:
            print(f'Entity: {ent.text}, Label: {ent.label_}, Start: {ent.start_char}, End: {ent.end_char}')

        results = get_results(doc)

        verify_result(context, expected_results, results, transformer, *transformerArgs)
    return _verify_detection

# Detect components with NLP test case factory
@pytest.fixture
def detect_with_nlp(create_doc, verify_detection):
    def _detect_with_nlp(test, transformer=None, *transformerArgs):
        doc = create_doc(test.context['text'])
        doc = test.test_func(doc)
        
        verify_detection(test.context, doc, transformer, *transformerArgs, expected_results=test.expected_result)
    return _detect_with_nlp