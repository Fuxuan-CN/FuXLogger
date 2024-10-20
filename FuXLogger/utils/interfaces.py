
from abc import ABC, abstractmethod


class IHandler(ABC):
    @abstractmethod
    def handle(self, message):
        """
        you must implement this method to handle the message
        """
        pass