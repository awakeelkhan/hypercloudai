from abc import ABC, abstractmethod

class ModelAdapter(ABC):
    @abstractmethod
    def generate(self, messages, tools=None):
        pass

    @abstractmethod
    def stream(self, messages, tools=None):
        pass