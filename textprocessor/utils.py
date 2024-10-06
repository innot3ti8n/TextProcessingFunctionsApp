from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

class ConcurrentTaskRunner:
    def __init__(self):
        self.tasks = []

    def add_task(self, func, *args, **kwargs):
        self.tasks.append((func, args, kwargs))

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

def update_dictionary(dict: dict, key, value):
    if value:
        dict[key] = value

    return dict