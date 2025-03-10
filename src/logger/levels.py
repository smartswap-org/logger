import enum


class LogLevel(enum.IntEnum):
    FATAL = 100
    CRITICAL = 90
    ERROR = 80
    WARNING = 70
    NOTICE = 60
    INFO = 50
    DEBUG = 40
    TRACE = 30 