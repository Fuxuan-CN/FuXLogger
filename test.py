from FuXLogger import LogManager, Level, LogFormatter, StreamHandler , FileHandler

my_log_fmt = LogFormatter("{time} | {levelName:<7} | {module}:{function} | {file}:{line} | {message}") # 我习惯这样的格式

# 然后创建一个StreamHandler, 输出到控制台
console_handler = StreamHandler("console", Level.ON, my_log_fmt, colorize=True, enableXMLRender=True)
file_handler = FileHandler("file", Level.ON, my_log_fmt, filename="test.log") # 这样就可以了
logger = LogManager.getLogger("test", Level.ON, my_log_fmt, enqueue=True) # 启用enqueue, 不阻塞主线程
logger.addHandler(console_handler) # 添加到日志记录器
logger.addHandler(file_handler) # 添加到日志记录器

logger.trace("trace message")
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.fatal("fatal message")