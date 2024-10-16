import logging
import traceback
from ._abstract_task_runner import _AbstractTaskRunner

class PipelineTaskRunner(_AbstractTaskRunner):
    def input(self, data=None):
        self.__data = data

        return self

    def run_all(self):
        result = self.__data
        for func, args, kwargs in self._tasks:
            try:
                result = func(result, *args, **kwargs)
            except Exception as e:
                error_message = f"Task generated an exception: {e}"
                traceback_str = traceback.format_exc()
                detailed_error = f"{error_message}\n\n{traceback_str}"
                logging.error(detailed_error)
        return result
