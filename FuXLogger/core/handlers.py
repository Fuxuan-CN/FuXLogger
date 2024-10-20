from ..utils.interfaces import IHandler
from .LogBody import LogRecord
from .formatter import LogFormatter
from .loglevel import LogLevel
from ..utils import Render
from ..utils.exceptions import NotImplementedException
import threading
import sys
import socket
import queue

class Handler(IHandler):
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

class SocketHandler(Handler):
    """
    用户可以指定一个socket地址，然后将日志发送到指定的socket地址
    """
    def __init__(self, name: str, 
        level: LogLevel, 
        formatter: LogFormatter, 
        host: str, 
        port: int, 
        timeout: int = 1
    ) -> None:
        super().__init__(name, level, formatter)
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.process_queue = queue.Queue()
        self.failed_cache = queue.Queue()
        self.thread = threading.Thread(target=self.__handle)
        self.thread.start()

    def close(self) -> None:
        if self.sock:
           self.sock.close()

    def __send_message(self, message: str) -> None:
        try:
            self.sock.connect((self.host, self.port))
            self.sock.sendall(message.encode())
        except Exception as e:
            print(f"Error while sending message to socket: {e}")
            self.failed_cache.put(message)

    def __handle_failed_cache(self) -> None:
        while not self.failed_cache.empty():
            message = self.failed_cache.get()
            self.__send_message(message)

    def __handle(self) -> None:
        while threading.main_thread().is_alive():
            try:
                message = self.process_queue.get(block=False, timeout=10) # 指定超时时间避免忙等待
                self.__send_message(message)
            except queue.Empty:
                self.__handle_failed_cache()
            except Exception as e:
                print(f"Error while handling message: {e}")
                self.failed_cache.put(message)
        self.close() # close socket when main thread is not alive

    def handle(self, record: LogRecord) -> None:
        if record.level.level >= self.level.level:
            message = Render.removeTags(self.formatter.format(record))
            self.process_queue.put(message)
            
    

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