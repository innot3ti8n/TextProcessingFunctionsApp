from abc import ABC, abstractmethod

class _AbstractTaskRunner(ABC):
    def __init__(self):
        self.tasks = []

    def add_task(self, func, *args, **kwargs):
        self.tasks.append((func, args, kwargs))
        return self

    @abstractmethod
    def run_all(self):
        pass
