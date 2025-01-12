""" 日志文件处理器 """
import threading
from .handler_base import Handler
from ...utils import Render
from ...models.log_body import LogRecord
from ...models.log_level import LogLevel
from ..formatter import LogFormatter

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