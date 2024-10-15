# import conftest helpers

# Result args: 
    #   <comp_id>: Int, 
    #   <start>: Int, 
    #   <end>: Int, 
    #   <flag>: Int | None
from textprocessor_tests.test_utils.helpers import Result

# import module that contains function to be tested
from textprocessor.utils import parse_llm_markup

def test_parse_llm_markup(test, markup_tcf):
    test(
        parse_llm_markup
    ).given({
        'text': 'One sunny morning my mum and I were cleaning out our grandfather’s shed',
        'llm_markup': '''One sunny morning my <mark data="32,*">mum</mark> and I were cleaning out our grandfather’s shed'''
    }).expects(
        Result(32, 21, 24, None)
    ).using(
        markup_tcf
    )