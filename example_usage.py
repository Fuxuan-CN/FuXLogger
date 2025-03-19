import time
from datetime import timedelta

from FuXLogger import LogManager

# fmt = LogFormatter("{time} | {levelName:<8} | {name}.{module}.{function} | {file}:{line:03d} | {message}")
logger = LogManager.getLogger("test", enqueue=True)
# console_handler = StreamHandler("console", Level.ON, fmt, enableXMLRender=True, colorize=True)
# logger.addHandler(console_handler)

start = time.time()
for i in range(10000):
    logger.trace(f"This is a trace message {i}")
end = time.time()

elapsed = end - start
to_delta = timedelta(seconds=elapsed)

logger.info(f"Execution time: {to_delta}")
