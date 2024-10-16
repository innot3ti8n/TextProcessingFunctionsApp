import json
import logging
from textprocessor.process_manager import ProcessManager
from textprocessor.task_runners import ConcurrentTaskRunner

class PromptProcessor:
    def __init__(self, pm: ProcessManager):
        self.__pm = pm
        self.__runner = ConcurrentTaskRunner()

    def __process_with_llm(self, processor, prompts_data):
        runner = ConcurrentTaskRunner()

        def process_task(markup_id, prompt_config):
            try:
                prompt_config = json.loads(prompt_config)
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON for markup_id {markup_id}: {e}")
                return None

            try:
                processor.input(prompt_config=prompt_config)

                if markup_id == 1:
                    res = self.__pm.runWith(processor)
                elif markup_id == 2:
                    res = self.__pm.runWith(processor)

                return { f"markup_{markup_id}": res }
            except Exception as e:
                logging.error(f"Error processing markup_id {markup_id}: {e}")
                return None

        for prompt_data in prompts_data:
            runner.add_task(process_task, prompt_data.markup_id, prompt_data.prompt_config)

        res = runner.run_all()

        return [
            { "llm_annotated": [markup.get("markup_1") for markup in res if "markup_1" in markup] },
            { "llm_notes": [markup.get("markup_2") for markup in res if "markup_2" in markup] },
        ]

    def __process_with_nlp(self, processor, componnents_data):
        res = self.__pm.runWith(processor)

        nlp_annotated = []
        nlp_notes = []

        for text_element in res:
            markup_id = componnents_data[text_element['comp_id']].markup_id
            if markup_id == 1:
                nlp_annotated.append(text_element)
            elif markup_id == 2:
                nlp_notes.append(text_element)

        return [
            { "nlp_annotated": nlp_annotated },
            { "nlp_notes": nlp_notes }
        ]
    
    def attach_data(self, data: dict):
        self.__data = data

        return self

    def run(self):
        pm = self.__pm
        runner = self.__runner

        for processor in pm.processors:
            # If processing with llm
            if pm.processor_type(processor) == 'llm':
                runner.add_task(self.__process_with_llm, processor, self.__data.get("prompts_data"))

            # If processing with nlp
            if pm.processor_type(processor) == 'nlp':
                runner.add_task(self.__process_with_nlp, processor, self.__data.get("components_data"))

        res = runner.run_all()
        return res