from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from ._abstract_task_runner import _AbstractTaskRunner

class ConcurrentTaskRunner(_AbstractTaskRunner):
    def run_all(self):
        results = []
        with ThreadPoolExecutor() as executor:
            future_to_task = {executor.submit(func, *args, **kwargs): (func, args, kwargs) for func, args, kwargs in self.tasks}
            for future in as_completed(future_to_task):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.error(f"Task generated an exception: {e}")
        return results
