
import uuid
from .exceptions import LogQueueEmptyException , LogQueueFullException
import queue
from ..core.LogBody import LogRecord

class LogQueue:
    """
    日志缓冲队列
    """
    def __init__(self, maxsize: int = 0):
        self.id = uuid.uuid4()
        self.maxsize = maxsize
        self.queue: queue.Queue[LogRecord] = queue.Queue(self.maxsize)

    def qsize(self):
        return self.queue.qsize()

    def empty(self):
        return self.queue.empty()

    def put(self, item: LogRecord, block: bool = True, timeout: float = 0.0) -> None:
        if self.maxsize > 0 and self.qsize() >= self.maxsize:
            raise LogQueueFullException("Log queue is full")
        self.queue.put(item, block, timeout)

    def get(self, block: bool = True, timeout: float = 0.0) -> LogRecord:
        try:
            return self.queue.get(block, timeout)
        except queue.Empty:
            raise LogQueueEmptyException("Log queue is empty")
        
    def __len__(self) -> int:
        return self.qsize()
    
    def __repr__(self) -> str:
        return f"<LogQueue id={self.id} maxsize={self.maxsize} qsize={self.qsize()}>"
    
    def __str__(self) -> str:
        return f"LogQueue(id={self.id}, maxsize={self.maxsize}, qsize={self.qsize()})"
    
    def __add__(self, other: "LogQueue") -> "LogQueue":
        if not isinstance(other, LogQueue):
            raise TypeError(f"unsupported operand type(s) for +: 'LogQueue' and '{type(other).__name__}'")
        new_queue = LogQueue(maxsize=self.maxsize + other.maxsize)
        while not self.empty():
            new_queue.put(self.get())
        while not other.empty():
            new_queue.put(other.get())
        return new_queue
    
    def __hash__(self) -> int:
        return hash(self.id)