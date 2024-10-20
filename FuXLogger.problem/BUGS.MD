
# 我这个FuXLogger的神奇bug

![BUGS](https://media.tenor.com/Ky5De2QfmrsAAAAi/fu-xuan-honkai-star-rail.gif)

## 如下

### 2024-10-5(bug 1. 日志库莫名其妙丢日志问题)

我像往常一样,测试我写的日志库有没有正常运行:

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

下面是输出:

```bash
2024-10-05 23:27:49 | TRACE   | __main__:<module> | test.py:13 | trace message
2024-10-05 23:27:49 | DEBUG   | __main__:<module> | test.py:14 | debug message
```

有时候还会输出:

```bash
2024-10-05 23:28:22 | TRACE   | __main__:<module> | test.py:13 | trace message
2024-10-05 23:28:22 | DEBUG   | __main__:<module> | test.py:14 | debug message
2024-10-05 23:28:22 | INFO    | __main__:<module> | test.py:15 | info message
```

但是INFO以上的日志记录却没有了, 这让我感到很意外，我又单独测试了下代码:

```python
logger.fatal("fatal message")
```

```bash
2024-10-05 23:28:22 | FATAL   | __main__:<module> | test.py:16 | fatal message
```

可以看到输出了，说明没有级别的问题。

神奇的是,当我把filehandler不添加进去的时候, 日志就正常了:

```bash
2024-10-05 23:30:02 | TRACE   | __main__:<module> | test.py:13 | trace message
2024-10-05 23:30:02 | DEBUG   | __main__:<module> | test.py:14 | debug message
2024-10-05 23:30:02 | INFO    | __main__:<module> | test.py:15 | info message
2024-10-05 23:30:02 | WARNING | __main__:<module> | test.py:17 | warning message
2024-10-05 23:30:02 | ERROR   | __main__:<module> | test.py:18 | error message
2024-10-05 23:30:02 | FATAL   | __main__:<module> | test.py:16 | fatal message
```

总而言之,就是会在filehandler和streamhandler都加进去,并且同时开启了enqueue选项的时候, 导致日志丢失的问题。

但是，我写了如下代码:

```python
for i in range(100):
    logger.trace("trace message")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.fatal("fatal message")
```

我却能看到循环运行的时候，日志记录是正常且完整的，但是循环的开始和最后的部分，日志记录却不完整，我就觉得很神奇！
