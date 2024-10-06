from collections import namedtuple
import json
import logging

from textprocessor.postprocessing import markup_text, transform_mark_data, merge_markups
from textprocessor.utils import ConcurrentTaskRunner

Flag = namedtuple('Flag', ['colour', 'characters'])
ComponentData = namedtuple('ComponentData', ['name', 'markup_id'])
Process = namedtuple('Process', ['skill_id', 'skill_processor'])
PromptData = namedtuple('PromptData', ['prompt_id', 'prompt_config', 'markup_id', 'handle_comps'])

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


def process_with_llm(pm: ProcessManager, processor, prompts_data, metadata):
    result = dict()
    runner = ConcurrentTaskRunner()

    def process_task(markup_id, prompt_config):
        try:
            payload = {'prompt_config': json.loads(prompt_config)}
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON for markup_id {markup_id}: {e}")
            return None

        try:
            if markup_id == 1:
                res = pm.runWith(processor, payload)
                return res
            elif markup_id == 2:
                res = pm.runWith(processor, payload)
                result['llm_notes'] = res
        except Exception as e:
            logging.error(f"Error processing markup_id {markup_id}: {e}")
            return None

    # Add tasks to the runner
    for prompt_data in prompts_data:
        runner.add_task(process_task, prompt_data.markup_id, prompt_data.prompt_config)

    # Run all tasks concurrently
    markups_res = runner.run_all()
    markups = [res for res in markups_res if res is not None]

    try:
        result['llm_annotated'] = transform_mark_data(merge_markups(pm.getContext("text"), markups), metadata)
    except Exception as e:
        logging.error(f"Error merging markups: {e}")
        result['llm_annotated'] = None

    return result

def process_with_nlp(pm: ProcessManager, processor, metadata):
    result = markup_text(pm.getContext("text"), pm.runWith(processor), metadata)
    
    return result