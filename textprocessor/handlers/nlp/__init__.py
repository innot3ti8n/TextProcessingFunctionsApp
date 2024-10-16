import spacy
from spacy.tokens import Doc
import importlib

from textprocessor.utils import get_results, get_constants

from textprocessor.handlers._ai_handler import _AIHandler
from .constants import component_constant_map as map
from textprocessor.data_models import ComponentConfig

from .punctuation import *

class NLPHandler(_AIHandler):
    def __init__(self):
        super().__init__("nlp")
        self.__nlp = spacy.load("en_core_web_sm")
        self.__default_pipe_names = self.__nlp.pipe_names
        Doc.set_extension("results", default=[], force=True)

    def input(self, text=None):
        if text: self.__text = text

        return self

    def add_custom_components(self, component_config: ComponentConfig):        
        handler_module_name = component_config.handler_module_name
        component_names = component_config.component_names

        # Clear existing custom pipes
        pipe_names = self.__nlp.pipe_names[:]
        for pipe_name in pipe_names:
            if pipe_name not in self.__default_pipe_names:
                self.__nlp.remove_pipe(pipe_name)

        # Import the handler module to register components
        importlib.import_module(f".{handler_module_name}", package=__package__)

        if not component_names:
            constants_module = importlib.import_module(f".constants.{map[handler_module_name]}", package=__package__)
            component_names = get_constants(constants_module)

        for component_name in component_names:
            # Import all component functions from the handler module and register globally
            self.__nlp.add_pipe(component_name, last=True)
        
        return self
    


    def process_text(self):
        doc = self.__nlp(self.__text)

        # Access the results
        results = get_results(doc)

        return results
    
__all__ = [
    'NLPHandler',
]
