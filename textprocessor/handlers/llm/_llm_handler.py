import json
import logging
import time

from .._ai_handler import _AIHandler

class _LLMHandler(_AIHandler):
    def __init__(self, llm_client):
        super().__init__("llm")
        self._client = llm_client
        self.reset_configs()
        

    def input(self, text=None, prompt_config=None):
        if text: self._text = text
        if prompt_config: self._prompt_config = prompt_config

        return self

    def config(self, options: dict):
        self._options.update(options)
                
        return self
    
    def reset_configs(self):
        self._options = {
            "retries": 3,
            "delay": 2
        }
    
    def attempt_request(self, send_request):
        retries = self._options.get('retries')
        delay = self._options.get('delay')

        for attempt in range(retries):
            try:
                return send_request()

            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {e}")
                return "Error: Invalid JSON in prompt configuration."

            except KeyError as e:
                logging.error(f"Missing key in prompt configuration: {e}")
                return f"Error: Missing key in prompt configuration: {e}"

            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    return "Error: An unexpected error occurred after multiple attempts."

