from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import traceback
from ._abstract_task_runner import _AbstractTaskRunner

class ConcurrentTaskRunner(_AbstractTaskRunner):
    def run_all(self):
        results = []
        with ThreadPoolExecutor() as executor:
            future_to_task = {executor.submit(func, *args, **kwargs): (func, args, kwargs) for func, args, kwargs in self._tasks}
            for future in as_completed(future_to_task):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    error_message = f"Task generated an exception: {e}"
                    traceback_str = traceback.format_exc()
                    detailed_error = f"{error_message}\n\n{traceback_str}"
                    logging.error(detailed_error)
        return results
