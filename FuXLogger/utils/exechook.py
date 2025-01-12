""" 格式化异常信息 """

import traceback
import multiprocessing
import threading
from typing import Optional
import inspect
import sys
from .type_hints import OptExcInfo

sys.exc_info()

def format_stack_trace(exctype, value, tb, max_depth=15, nested=False):
    tb_list = traceback.extract_tb(tb)
    exception_info = ""

    if nested:
        exception_info = f"{exctype.__name__}: {value}\n"
    else:
        # 获取当前进程和线程名称
        process_name = multiprocessing.current_process().name
        thread_name = threading.current_thread().name
        exception_info = f"Exception in process: {process_name}, thread: {thread_name}; {exctype.__name__}: {value}\n"
        exception_info += "Traceback (most recent call last):\n"

    # 限制堆栈跟踪的深度
    limited_tb_list = tb_list[:max_depth]
    more_frames = len(tb_list) - max_depth

    for i, (filename, lineno, funcname, line) in enumerate(limited_tb_list):
        # 获取函数所在的模块名
        module_name = inspect.getmodulename(filename)
        exception_info += f"  at {module_name}.{funcname} in ({filename}:{lineno})\n"

    if more_frames > 0:
        exception_info += f"  ... {more_frames} more ...\n"

    # 检查是否有原因和其他信息
    cause = getattr(value, '__cause__', None)
    context = getattr(value, '__context__', None)
    
    if cause:
        exception_info += "Caused by: "
        exception_info += format_stack_trace(type(cause), cause, cause.__traceback__, nested=True)
    if context and not cause:
        exception_info += "Original exception: "
        exception_info += format_stack_trace(type(context), context, context.__traceback__, nested=True)
    
    return exception_info

def ExtractException(excinfo: OptExcInfo) -> Optional[str]:
    # 获取回溯信息并格式化为字符串
    if excinfo is None:
        return None
    tb_str = format_stack_trace(excinfo[0], excinfo[1], excinfo[2])
    
    # 记录异常信息到日志
    exception_info = ""
    exception_info += tb_str
    # 返回异常信息
    return exception_info

def sys_excepthook(excinfo: OptExcInfo):
    # 获取异常信息并打印到控制台
    exception_info = ExtractException(excinfo)
    colored = f"\033[1;31m{exception_info}\033[0m"
    print(colored, file=sys.stderr)

def set_exechook():
    """
    设置全局异常处理函数
    """
    sys.excepthook = sys_excepthook

def GetStackTrace(vokedepth: int = 1) -> str:
    """
    获取堆栈跟踪信息
    """
    # 获取当前调用栈信息的前两层
    stack = traceback.extract_stack(limit=vokedepth)
    stack_info = "Stack Trace:\n"
    for frame in stack[:-vokedepth+1]:
        filename = frame.filename
        line = frame.lineno
        funcname = frame.name
        stack_info += f"  at {funcname} in ({filename}:{line})\n"
    return stack_info