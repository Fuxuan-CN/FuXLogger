import asyncio
from .loglevel import Level , LogLevel , addlevel
from .handlers import Handler
from .LogBody import LogRecord
from ..utils import ExtractException
from ..utils.excformat import GetStackTrace
from ..utils.timeutil import getLocalDateTime, getUTCDateTime
from ..utils.exceptions import InvalidConfigurationException
from ..utils._typeInfo import Message
from ..utils.exceptions import InvalidEnvironmentException
from ..utils.LogQueue import LogQueue , LogQueueEmptyException
import threading
import multiprocessing
import os
import sys
import uuid
import inspect

class Logger:
    def __init__(self, name: str, level: LogLevel, handlers: set[Handler] = set(), enqueue: bool = False, is_async: bool = False, only_handler: bool = False):
        self.name: str = name
        self.level: LogLevel = level
        self.handlers: set[Handler] = handlers
        self.enqueue: bool = enqueue
        self.is_async: bool = is_async
        self.uuid = uuid.uuid4()
        self.only_handler: bool = only_handler
        if enqueue and is_async:
            raise InvalidConfigurationException("Cannot use enqueue and is_async at the same time")
        if enqueue:
            self.queue = LogQueue()
            self.log_thread = threading.Thread(target=self.__enqueueHandler, daemon=True)
            self.log_thread.start()
        elif is_async:
            try:
                self.async_queue = asyncio.Queue()
                self.loop = asyncio.get_running_loop()
                self.start_async_logging()
            except RuntimeError as caused_by:
                raise InvalidEnvironmentException("Cannot use is_async outside of an asyncio event loop") from caused_by

    def start_async_logging(self):
        if not self.is_async:
            return
        self.log_task = self.loop.create_task(self.__async_enqueueHandler())

    def stop_async_logging(self):
        if self.is_async and self.log_task:
            self.log_task.cancel()
            try:
                self.loop.run_until_complete(self.log_task)
            except asyncio.CancelledError:
                pass
            except RuntimeError:
                pass
            self.log_task = None

    def close(self) -> None:
        """
        清理资源的时候调用
        """
        if self.enqueue:
            self.log_thread.join()
        elif self.is_async:
            self.stop_async_logging()
        else:
            pass

    def addLevel(self, level: LogLevel) -> None:
        addlevel(level)

    def setLevel(self, level: LogLevel) -> None:
        self.level = level

    def addHandler(self, handler: Handler) -> None:
        self.handlers.add(handler)

    def removeHandler(self, handler: Handler) -> None:
        self.handlers.remove(handler)

    async def __async_enqueueHandler(self) -> None:
        while True:
            try:
                async with asyncio.Lock():
                    record = await asyncio.wait_for(self.async_queue.get(), timeout=0.1)
                    for handler in self.handlers:
                        await asyncio.to_thread(handler.handle, record)
                    self.async_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    def __enqueueHandler(self) -> None:
        while True:
            try:
                record = self.queue.get(timeout=0.1)
                for handler in self.handlers:
                    handler.handle(record)
            except LogQueueEmptyException:
                if not threading.main_thread().is_alive():
                    break
                continue

    def __makeRecord(self, message: Message, level: LogLevel) -> LogRecord:
        frame = inspect.currentframe().f_back.f_back.f_back  # type: ignore
        levelname = level.name
        current_module = inspect.getmodule(frame)
        module = current_module.__name__ if current_module else "__main__"
        return LogRecord(
            name=self.name,
            level=level,
            levelName=levelname,
            time="", # 留给后面格式化处理
            timestamp=getLocalDateTime(),
            utctime=getUTCDateTime(),
            threadid=threading.get_ident(),
            processid=multiprocessing.current_process().pid,  # type: ignore
            processName=multiprocessing.current_process().name,
            threadName=threading.current_thread().name,
            stack_info=GetStackTrace(5),
            file=os.path.basename(frame.f_code.co_filename),  # type: ignore
            pathname=frame.f_code.co_filename, # type: ignore
            workdir=os.getcwd(),
            line=frame.f_lineno,  # type: ignore
            function=frame.f_code.co_name,  # type: ignore
            module=module,  # type: ignore
            message=message
        )

    def __log(self, level: LogLevel, message: Message) -> None:
        """
        记录一个日志的内部实现
        """
        if self.enqueue:
            self.queue.put(self.__makeRecord(message, level))
        elif self.is_async:
            self.async_queue.put_nowait(self.__makeRecord(message, level))
        else:
            for handler in self.handlers:
                handler.handle(self.__makeRecord(message, level))

    def exception(self, message: str, is_fatal: bool = False) -> None:
        """
        记录异常信息到日志,如果没有异常发生,这个只会记录一个ERROR级别的日志(取决于是否设置了is_fatal),如果有,则会带上堆栈信息
        - is_fatal: 是否是致命错误,如果是,则会记录FATAL级别的日志,否则记录ERROR级别的日志
        """
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if exc_traceback is not None:
            exc_info = ExtractException(exc_type, exc_value, exc_traceback)
            if is_fatal:
                self.__log(Level.FATAL, f"{message}\n{exc_info}")
            else:
                self.__log(Level.ERROR, f"{message}\n{exc_info}")
        elif is_fatal:
            self.__log(Level.FATAL, message)
        else:
            self.__log(Level.ERROR, message)

    def log(self, level: LogLevel, message: Message) -> None:
        """
        记录一个 {level} 级别的日志
        """
        self.__log(level, message)

    def trace(self, message: Message) -> None:
        """
        记录一个 TRACE 级别的日志
        """
        self.__log(Level.TRACE, message)

    def debug(self, message: Message) -> None:
        """
        记录一个 DEBUG 级别的日志
        """
        self.__log(Level.DEBUG, message)

    def info(self, message: Message) -> None:
        """
        记录一个 INFO 级别的日志
        """
        self.__log(Level.INFO, message)

    def warning(self, message: Message) -> None:
        """
        记录一个 WARN 级别的日志
        """
        self.__log(Level.WARN, message)

    def error(self, message: Message) -> None:
        """
        记录一个 ERROR 级别的日志
        """
        self.__log(Level.ERROR, message)

    def fatal(self, message: Message) -> None:
        """
        记录一个 FATAL 级别的日志
        """
        self.__log(Level.FATAL, message)