from typing import Union
from types import TracebackType

Message = Union[str, bytes]
""" 日志消息的类型提示 """

OptExcInfo = tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]
""" 异常信息的类型提示 """