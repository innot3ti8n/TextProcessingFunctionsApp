import json
import logging
from textprocessor.process_manager import ProcessManager
from textprocessor.task_runners import ConcurrentTaskRunner

class PromptProcessor:
    def __init__(self, pm: ProcessManager):
        self.pm = pm
        self.process_with = None

    def process_with_llm(self, processor, prompts_data):
        self.process_with = self.pm.processor_type(processor)

        runner = ConcurrentTaskRunner()

        def process_task(markup_id, prompt_config):
            try:
                payload = {'prompt_config': json.loads(prompt_config)}
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON for markup_id {markup_id}: {e}")
                return None

            try:
                if markup_id == 1:
                    res = self.pm.runWith(processor, payload)
                elif markup_id == 2:
                    res = self.pm.runWith(processor, payload)

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

    def process_with_nlp(self, processor):
        self.process_with = self.pm.processor_type(processor)

        return [{ "nlp_annotated": self.pm.runWith(processor) }]
    
    @property
    def isProcessedWith(self, processor_type):
        return self.process_with == processor_type