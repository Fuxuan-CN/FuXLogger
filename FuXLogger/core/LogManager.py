from .logger import Logger
from .formatter import LogFormatter
from .handlers import StreamHandler
from ..models.log_level import Level, LogLevel
import threading
import atexit


class LogManager:
    loggers: dict[str, Logger] = {}
    defaultFormatter: LogFormatter = LogFormatter(
        "{time} | {levelName:<8} | {name}.{module}.{function} | {file}:{line:03d} | {message}")
    lock = threading.Lock()

    @staticmethod
    def getLogger(name: str = 'default', level_threshold: LogLevel = Level.ON,
                  formatter: LogFormatter = defaultFormatter, enqueue: bool = False, is_async: bool = False) -> Logger:
        """
        获取一个日志记录器对象,注意,如果is_async为True,则确保必须在异步环境内调用此方法,否则会报错
        """
        default_handler = StreamHandler('default', level_threshold, formatter, colorize=True, enableXMLRender=True)
        with LogManager.lock:
            if LogManager.loggers.get(name) is None:
                LogManager.loggers[name] = Logger(name=name, handlers=default_handler, enqueue=enqueue,
                                                  is_async=is_async)
            return LogManager.loggers[name]

    @staticmethod
    def closeAll():
        """
        关闭所有日志记录器
        """
        with LogManager.lock:
            for logger in LogManager.loggers.values():
                logger.close()
            LogManager.loggers.clear()

    @staticmethod
    def registerExitHandler():
        """
        注册退出处理器,在程序退出时自动关闭所有日志记录器
        """
        atexit.register(LogManager.closeAll)


LogManager.registerExitHandler()
