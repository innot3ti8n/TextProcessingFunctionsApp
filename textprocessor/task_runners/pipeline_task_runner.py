import logging
from ._abstract_task_runner import _AbstractTaskRunner

class PipelineTaskRunner(_AbstractTaskRunner):
    def run_all(self):
        results = []
        for func, args, kwargs in self.tasks:
            try:
                if results:
                    kwargs['previous_result'] = results[-1]
                result = func(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logging.error(f"Task generated an exception: {e}")
        return results
