# import required modules
import pytest
import spacy
from spacy.tokens import Doc

@pytest.fixture(scope="module")
def nlp():
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Register custom attributes
    Doc.set_extension("results", default=[], force=True)

    return nlp

@pytest.fixture
def create_doc(nlp):
    def _create_doc(text):
        doc = nlp(text)
        
        return doc
    return _create_doc