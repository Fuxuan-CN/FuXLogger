
# 更新日志

![FuXLogger](https://media.tenor.com/A11YI0qGHRoAAAAi/fu-xuan-honkai-star-rail.gif)

## v0.2.7.post2 (2024-10-16 22:01)

- ***修复了FuXLogger.utils.types模块导入的错误(会再其他库下用的话构建失败的问题), 现在更名为 FuXLogger.utils._typeInfo***

## v0.2.7.post1 (2024-10-14 18:39)

- ***修复了添加等级的bug***

## v0.2.7 (2024-10-14 18:17)

- ***完善了日志等级管理***

## v0.2.6 (2024-10-13 14:03)

- ***修复了因为类型定义版本不同导致的报错***

## v0.2.5 (2024-10-1 12:44)

- ***添加了关于日志库的类型注解,使得代码更可读***

## v0.2.4 (2024-9-28 17:27)

- ***添加异常类 InvaildEnvironmentException, 用于表示在错误的环境运行时抛出异常***

## v0.2.3 (2024-9-28 16:56)

- ***添加 {workdir} 变量到 LogFormatter, 用于获取当前工作目录***

## v0.2.2 (2024-9-28)

- ***logger.exception()方法改进, 添加了is_fatal参数, 用于用户确认此异常是否为致命错误, 并将其写入日志***

## v0.2.1 (2024-9-26)

- ***修复了一些bug***

## v0.2.0 (2024-9-25)

- ***实现异步记录日志功能,示例代码如下***

```python
from FuXLogger import LogManager , LogLevel , StreamHandler , LogFormatter
import asyncio

async def main():
    my_log_fmt = LogFormatter("{time} | {levelName:<7} | {module}:{function} | {file}:{line:02} | {message}")
    logger = LogManager.getLogger("main", my_log_fmt, False, True)

    console_handler = StreamHandler("console", LogLevel.TRACE, my_log_fmt,colorize=True, enableXMLRender=True)

    logger.addHandler(console_handler)

    logger.trace("trace message")
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.fatal("fatal message")
    await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
```

## v0.1.0 (2024-9-24)

- 实现基本功能
