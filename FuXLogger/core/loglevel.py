from typing import Optional
from ..utils.color import Color , Font

class LogLevel:
    """
    日志中表示等级的类
    """
    def __init__(self, name: str, level: int | float, color: Optional[Color] = None, font: Optional[Font] = None) -> None:
        self.name = name
        self.level = level
        self.color = color
        self.font = font

    def __str__(self) -> str:
        return f"{self.name} ({self.level})"
    
    def __repr__(self) -> str:
        return f"LogLevel(name='{self.name}', level={self.level})"
    
class Level:
    """
    日志等级类
    """
    ON = LogLevel("ON", float('-inf'))
    TRACE = LogLevel("TRACE", 1, Color.GREY, Font.BOLD)
    DEBUG = LogLevel("DEBUG", 2, Color.BLUE, Font.BOLD)
    INFO = LogLevel("INFO", 3, Color.CYAN, Font.BOLD)
    WARN = LogLevel("WARN", 4, Color.YELLOW, Font.BOLD)
    ERROR = LogLevel("ERROR", 5, Color.RED, Font.BOLD)
    FATAL = LogLevel("FATAL", 6, Color.PURPLE, Font.BOLD)
    OFF = LogLevel("OFF", float('inf'))
    
_str_to_level = {
    "ON": Level.ON,
    "TRACE": Level.TRACE,
    "DEBUG": Level.DEBUG,
    "INFO": Level.INFO,
    "WARN": Level.WARN,
    "ERROR": Level.ERROR,
    "FATAL": Level.FATAL,
    "OFF": Level.OFF
}

_level_to_str = {
    Level.ON: "ON",
    Level.TRACE: "TRACE",
    Level.DEBUG: "DEBUG",
    Level.INFO: "INFO",
    Level.WARN: "WARN",
    Level.ERROR: "ERROR",
    Level.FATAL: "FATAL",
    Level.OFF: "OFF"
}

def addlevel(level: LogLevel) -> None:
    """
    添加日志等级
    """
    _str_to_level[level.name] = level
    _level_to_str[level] = level.name

def getLevel(name: str) -> LogLevel:
    """
    获取日志等级
    """
    return _str_to_level[name]

def getLevelName(level: LogLevel) -> str:
    """
    获取日志等级名称
    """
    return _level_to_str[level]