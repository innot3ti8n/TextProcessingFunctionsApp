import spacy
from spacy.tokens import Doc

def get_nlp(component_names=None):
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Register custom attributes
    Doc.set_extension("results", default=[], force=True)

    if component_names:
        for component_name in component_names:
            nlp.add_pipe(component_name, last=True)

    return nlp

def get_results(doc):
    return doc._.results

def set_results(doc, value):
    doc._.results = value