""" 日志网络发送模块 """
import socket
import threading
import queue
from ...models.log_body import LogRecord
from ..formatter import LogFormatter
from ...models.log_level import LogLevel
from ...utils import Render
from .handler_base import Handler

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