
from ...exceptions import NotImplementedException
from ...utils.interfaces import IHandler
from ...models.log_level import LogLevel
from ..formatter import LogFormatter
from ...models.log_body import LogRecord

class Handler(IHandler):
    """ Base class for all handlers """
    def __init__(self,
        name: str,
        level: LogLevel,
        formatter: LogFormatter
    ) -> None:
        self.name = name
        self.level = level
        self.formatter = formatter

    def handle(self, record: LogRecord) -> None:
        raise NotImplementedException("handle method not implemented")


    def __str__(self):
        return f'{self.__class__}(name={self.name}, levelThreshold={self.level}, formatter={self.formatter})'

