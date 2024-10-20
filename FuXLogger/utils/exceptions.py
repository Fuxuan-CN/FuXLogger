
class FuXLoggerException(Exception):
    """
    Base class for all FuXLogger exceptions.
    """
    pass

class RendererException(FuXLoggerException):
    """
    Exception raised when there is an error in the rendering process.
    """
    pass

class NotImplementedException(FuXLoggerException):
    """
    Exception raised when a method or function is not implemented yet.
    """
    pass

class InvalidConfigurationException(FuXLoggerException):
    """
    Exception raised when there is an error in the configuration file.
    """
    pass

class InvalidHandlerException(FuXLoggerException):
    """
    Exception raised when there is an error in the handler configuration.
    """
    pass

class InvalidEnvironmentException(FuXLoggerException):
    """
    Exception raised when there is an error in the environment configuration.
    example: if you open the 'is_async' option ,but you running in sync mode, you will get this exception.
    """
    pass

class LogQueueEmptyException(FuXLoggerException):
    """
    Exception raised when the log queue is empty and there is no log to be processed.
    """
    pass

class LogQueueFullException(FuXLoggerException):
    """
    Exception raised when the log queue is full and there is no space to add new logs.
    """
    pass