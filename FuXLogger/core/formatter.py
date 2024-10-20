from .LogBody import LogRecord
import datetime

class LogFormatter:
    """
    日志格式化器
    ## 新日志库的格式如下:
    - {time}: 时间
    - {level}: 日志级别的INT值
    - {levelName}: 日志级别的名称
    - {message}: 日志信息
    - {module}: 日志所在模块
    - {file}: 日志所在文件名
    - {line}: 日志所在行号
    - {function}: 日志所在函数名
    - {processid}: 进程ID
    - {threadid}: 线程ID
    - {threadName}: 线程名
    - {processName}: 进程名
    - {pathname}: 日志所在文件路径
    - {workdir}: 当前工作目录
    - {timestamp}: 日志本地时间戳
    - {utctime}: 日志UTC时间戳
    - {Stack}: 日志堆栈信息
    """
    def __init__(self, format: str, datefmt: str = "%Y-%m-%d %H:%M:%S") -> None:
        self._format = format
        self._datefmt = datefmt

    def setFormatter(self, format: str, datefmt: str = "%Y-%m-%d %H:%M:%S") -> None:
        """
        设置日志格式化器
        :param format: 日志格式
        :param datefmt: 时间格式
        :return: None
        """
        self._format = format
        self._datefmt = datefmt

    def format(self, record: LogRecord) -> str:
        """
        格式化日志记录
        :param record: 日志记录字典
        :return: 格式化后的日志字符串
        """
        record_copy = record.ToDict()
        record_copy['timestamp'] = datetime.datetime.fromtimestamp(record.timestamp)
        record_copy['time'] = record_copy['timestamp'].strftime(self._datefmt)
        formatted_msg = self._format.format(**record_copy)
        return formatted_msg