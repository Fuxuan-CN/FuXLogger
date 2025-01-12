from ...models.log_body import LogRecord
from ..formatter import LogFormatter
from ...models.log_level import LogLevel
from ...utils import Render
from .handler_base import Handler
import threading
import sys

class StreamHandler(Handler):
    def __init__(self, name: str, 
        level: LogLevel, 
        formatter: LogFormatter, 
        stream=sys.stdout, 
        colorize: bool = False,
        enableXMLRender: bool = False
    ) -> None:
        super().__init__(name, level, formatter)
        self.stream = stream
        self.colorize = colorize
        self.enableXMLRender = enableXMLRender

    def write(self, message: str) -> None:
        self.stream.write(message)
        self.stream.flush()

    def handle(self, record: LogRecord) -> None:
        if record.level.level >= self.level.level:
            if self.colorize and self.enableXMLRender:
                color = record.level.color
                record.message = Render.renderWithXML(record.message)
                renderedMsg = Render.render(self.formatter.format(record), color, record.level.font) # type: ignore
                self.write(f"{renderedMsg}\n")
            elif self.colorize:
                color = record.level.color
                renderedMsg = Render.render(self.formatter.format(record), color, record.level.font) # type: ignore
                self.write(f"{renderedMsg}\n")
            else:
                self.write(f"{self.formatter.format(record)}\n")

class FileHandler(Handler):
    def __init__(self, name: str, 
        level: LogLevel, 
        formatter: LogFormatter, 
        filename: str, 
        mode: str = "a", 
        encoding: str = "utf-8",
    ) -> None:
        super().__init__(name, level, formatter)
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.lock = threading.Lock()

    def handle(self, record: LogRecord) -> None:
        if record.level.level >= self.level.level:
            with self.lock:
                with open(self.filename, self.mode, encoding=self.encoding) as f:
                    f.write(f"{Render.removeTags(self.formatter.format(record))}\n")