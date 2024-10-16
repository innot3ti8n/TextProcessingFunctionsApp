from abc import ABC, abstractmethod

class _AIHandler(ABC):
    def __init__(self, handler_type):
        self._handler_type = handler_type

    @abstractmethod   
    def input(self):
        pass

    @abstractmethod
    def process_text(self):
        pass

    @property
    def handler_type(self):
        return self._handler_type