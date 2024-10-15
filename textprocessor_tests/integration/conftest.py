# import required modules
import pytest
from textprocessor.utils import get_results
from textprocessor.utils import markup_text

# import fixtures
from textprocessor_tests.test_utils.fixtures import conn, get_skill_data, verify_result, test
from textprocessor_tests.test_utils.nlp_fixtures import nlp, create_doc

class Marker:
    def __init__(self, comp_name, comp_index, flag_text=None, flag_colour=None):
        self.comp_name = comp_name
        self.comp_index = comp_index
        self.flag_text = flag_text or "\u2003"
        self.flag_colour = flag_colour
        self.has_flag = flag_colour is not None

    def withContent(self, content):
        if self.has_flag:
            opening_mark = f"""<mark class="highlight flag" data-component-name="{self.comp_name}" data-subcomponent-text="{self.flag_text}" style="--component-background: var(--c{self.comp_index}-background); --subcomponent-background: {self.flag_colour}">"""
        else:
            opening_mark = f"""<mark class="highlight" data-component-name="{self.comp_name}" style="--component-background: var(--c{self.comp_index}-background)">"""
        
        return f"{opening_mark}{content}</mark>"

@pytest.fixture
def mark():
    def _mark(comp_name, comp_index, flag_text=None, flag_colour=None):
        return Marker(comp_name, comp_index, flag_text, flag_colour)
    return _mark

# Detect and markup NLP component test case factory
@pytest.fixture
def detect_markup_nlp_comp(create_doc, get_skill_data, verify_result):
    def _detect_markup_nlp_comp(test, transformer, *transformerArgs):
        doc = create_doc(test.context['text'])    
        doc = test.test_func(doc)

        metadata = get_skill_data(test.context['skill_id'])

        del metadata["prompts_data"]
        
        verify_result(
            test.context,
            test.expected_result,
            markup_text(test.context['text'], get_results(doc), metadata),
            transformer, 
            transformerArgs
        )

    return _detect_markup_nlp_comp