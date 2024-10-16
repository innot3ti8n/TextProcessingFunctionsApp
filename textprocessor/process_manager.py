from dataclasses import dataclass
from .handlers._ai_handler import _AIHandler

@dataclass
class Process:
    skill_id: int
    skill_processor: _AIHandler

class ProcessManager:
    def __init__(self, *args: Process):
        self.__processors = []
        self.__processes = []
        self.__processes.extend(args)

    def load(self, skill_id):        
        for process in self.__processes:
            if process.skill_id == skill_id:
                self.__processors.append(process.skill_processor)
        return self
    
    def runWith(self, processor: _AIHandler):        
        if self.processor_type(processor) == 'nlp':
            return processor.process_text()
        elif self.processor_type(processor) == 'llm':
            return processor.process_text()

    def processor_type(self, processor: _AIHandler):
        return processor.handler_type
    
    @property
    def processors(self):
        return self.__processors
