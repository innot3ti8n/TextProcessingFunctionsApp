# import required
from textprocessor.utils import get_results

# import functions / module contains functions to test
from textprocessor.handlers.nlp import punctuation as punct

# Test cases
def test_detect_markup_proper_nouns(test, mark, detect_markup_nlp_comp):
    component_name = "capitalise proper noun"

    test(punct.detect_proper_nouns).given({
        'text': "John works at Google in New York.",
        'skill_id': 1
    }).expects(
        f"""{mark(component_name, 1, flag_colour="green").withContent("John")} works at {mark(component_name, 1, flag_colour="green").withContent("Google")} in {mark(component_name, 1, flag_colour="green").withContent("New York")}."""
    ).using(
        detect_markup_nlp_comp
    )

    test(punct.detect_proper_nouns).given({
        'text': "john works at Google in New York.",
        'skill_id': 1
    }).expects(
        f"""{mark(component_name, 1, flag_colour="red").withContent("john")} works at {mark(component_name, 1, flag_colour="green").withContent("Google")} in {mark(component_name, 1, flag_colour="green").withContent("New York")}."""
    ).using(
        detect_markup_nlp_comp
    )
        