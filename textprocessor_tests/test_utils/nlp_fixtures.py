# import required modules
import pytest
from textprocessor.skills.nlp import get_nlp

@pytest.fixture(scope="module")
def nlp():
    return get_nlp()

@pytest.fixture
def create_doc(nlp):
    def _create_doc(text):
        doc = nlp(text)
        
        return doc
    return _create_doc