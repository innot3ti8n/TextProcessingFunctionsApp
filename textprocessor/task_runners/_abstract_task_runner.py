from abc import ABC, abstractmethod

class _AbstractTaskRunner(ABC):
    def __init__(self):
        self._tasks = []

    def add_task(self, func, *args, **kwargs):
        self._tasks.append((func, args, kwargs))
        return self

    @abstractmethod
    def run_all(self):
        pass
