from collections import namedtuple

Process = namedtuple('Process', ['skill_id', 'skill_processor'])

class ProcessManager:
    def __init__(self, *args: Process):
        self.__processors = []
        self.__context = {}
        self.__processes = []
        self.__processes.extend(args)

    def createContext(self, skill_id, text):
        self.__context.setdefault("text", text)
        
        for process in self.__processes:
            if process.skill_id == skill_id:
                self.__processors.append(process.skill_processor)
        return self
    
    def runWith(self, processor, payload=None):
        text = self.getContext("text")

        if self.processor_type(processor) == 'nlp':
            return processor.process_text(text)
        elif self.processor_type(processor) == 'llm':
            return processor.process_text(text, payload['prompt_config'])

    def getContext(self, key):
        return self.__context[key]
    
    @property
    def processors(self):
        return self.__processors

    def processor_type(self, processor):
        return processor.__name__.split('.')[2]
