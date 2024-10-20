
# MY FuXLogger logging library bugs

![BUGS](https://media.tenor.com/Ky5De2QfmrsAAAAi/fu-xuan-honkai-star-rail.gif)

## ALL BUGS

### 2024-10-5 (bug1. log Incomplete with unknow reasons)

one day , I want make sure my logging-library FuXLogger is working normally, so I write a simple code to test it.

```python
from FuXLogger import LogManager, LogLevel, LogFormatter, StreamHandler , FileHandler

my_log_fmt = LogFormatter("{time} | {levelName:<7} | {module}:{function} | {file}:{line} | {message}") # 我习惯这样的格式

# 然后创建一个StreamHandler, 输出到控制台
console_handler = StreamHandler("console", LogLevel.ON, my_log_fmt, colorize=True, enableXMLRender=True)
file_handler = FileHandler("file", LogLevel.ON, my_log_fmt, filename="test.log") # 这样就可以了
logger = LogManager.getLogger("test",LogLevel.ON, my_log_fmt, enqueue=True) # 启用enqueue, 不阻塞主线程
logger.addHandler(console_handler) # 添加到日志记录器
logger.addHandler(file_handler) # 添加到日志记录器

logger.trace("trace message")
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.fatal("fatal message")
```

this is output:

```bash
2024-10-05 23:27:49 | TRACE   | __main__:<module> | test.py:13 | trace message
2024-10-05 23:27:49 | DEBUG   | __main__:<module> | test.py:14 | debug message
```

and output next:

```bash
2024-10-05 23:28:22 | TRACE   | __main__:<module> | test.py:13 | trace message
2024-10-05 23:28:22 | DEBUG   | __main__:<module> | test.py:14 | debug message
2024-10-05 23:28:22 | INFO    | __main__:<module> | test.py:15 | info message
```

my logging-library not logged level higher than INFO(some times not logged level higher than DEBUG) messages.
This is so excepted and I don't know why it happened.

so I test my class Logger method '{level}' is working normally. I test it one by one.

```python
logger.trace("trace message")
```

```python
logger.debug("debug message")
```

```python
logger.info("info message")
```

```python
logger.warning("warning message")
```

```python
logger.error("error message")
```

```python
logger.fatal("fatal message")
```

the output all of them:

```bash
2024-10-05 23:30:22 | TRACE   | __main__:<module> | test.py:13 | trace message
```

```bash
2024-10-05 23:30:22 | DEBUG   | __main__:<module> | test.py:14 | debug message
```

```bash
2024-10-05 23:30:22 | INFO    | __main__:<module> | test.py:15 | info message
```

```bash
2024-10-05 23:30:22 | WARNING | __main__:<module> | test.py:16 | warning message
```

```bash
2024-10-05 23:30:22 | ERROR   | __main__:<module> | test.py:17 | error message
```

```bash
2024-10-05 23:30:22 | FATAL   | __main__:<module> | test.py:18 | fatal message
```

all of them logged normally, so I think the bug is not in my templated __log method.

The amazing thing is that when I don't add the FileHandler in to logger, the logger is working fine!

```python
from FuXLogger import LogManager, LogLevel, LogFormatter, StreamHandler , FileHandler

my_log_fmt = LogFormatter("{time} | {levelName:<7} | {module}:{function} | {file}:{line} | {message}") # 我习惯这样的格式

# 然后创建一个StreamHandler, 输出到控制台
console_handler = StreamHandler("console", LogLevel.ON, my_log_fmt, colorize=True, enableXMLRender=True)
logger = LogManager.getLogger("test",LogLevel.ON, my_log_fmt, enqueue=True) # 启用enqueue, 不阻塞主线程
logger.addHandler(console_handler) # 添加到日志记录器

logger.trace("trace message")
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.fatal("fatal message")
```

```bash
2024-10-05 23:32:22 | TRACE   | __main__:<module> | test.py:13 | trace message
2024-10-05 23:32:22 | DEBUG   | __main__:<module> | test.py:14 | debug message
2024-10-05 23:32:22 | INFO    | __main__:<module> | test.py:15 | info message
2024-10-05 23:32:22 | WARNING | __main__:<module> | test.py:16 | warning message
2024-10-05 23:32:22 | ERROR   | __main__:<module> | test.py:17 | error message  
2024-10-05 23:32:22 | FATAL   | __main__:<module> | test.py:18 | fatal message
```

In short, when both FileHandler and StreamHandler are added, and the enqueue option is enabled at the same time, the log will Incomplete with unknow reasons.

but I write a loop code to test it:

```python
for i in range(100):
    logger.trace("trace message")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.fatal("fatal message")
```

The log working normally when the loop is running but the log Incomplete on loop start and end. I don't know why.
