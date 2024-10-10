from .dict_utils import update_dictionary
from .nlp_utils import keep_lowest_comp_index, get_nlp, get_results, set_results
from .markup_utils import markup_text, transform_mark_data, merge_markups

__all__ = [
    'update_dictionary', 
    
    'keep_lowest_comp_index', 
    'get_nlp', 
    'get_results', 
    'set_results',

    'markup_text',
    'transform_mark_data',
    'merge_markups'
]
