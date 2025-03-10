import enum
import datetime
import sys
import os
from typing import TextIO, Optional


class LogLevel(enum.IntEnum):
    FATAL = 100
    CRITICAL = 90
    ERROR = 80
    WARNING = 70
    NOTICE = 60
    INFO = 50
    DEBUG = 40
    TRACE = 30


class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    BRIGHT_RED = "\033[91m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"


class Logger:
    def __init__(self, output: TextIO = sys.stdout, min_level: LogLevel = LogLevel.INFO, log_to_file: bool = False, log_dir: str = "logs"):
        self.output = output
        self.min_level = min_level
        self.log_to_file = log_to_file
        self.log_dir = log_dir
        self.file_handle = None
        self._log_date = None
        
        self._level_colors = {
            LogLevel.FATAL: f"{Colors.BOLD}{Colors.BRIGHT_RED}",
            LogLevel.CRITICAL: Colors.BRIGHT_RED,
            LogLevel.ERROR: Colors.RED,
            LogLevel.WARNING: Colors.YELLOW,
            LogLevel.NOTICE: Colors.GREEN,
            LogLevel.INFO: Colors.BLUE,
            LogLevel.DEBUG: Colors.MAGENTA,
            LogLevel.TRACE: Colors.GRAY,
        }
        
        self._level_names = {
            LogLevel.FATAL: "FATAL",
            LogLevel.CRITICAL: "CRITICAL",
            LogLevel.ERROR: "ERROR",
            LogLevel.WARNING: "WARNING",
            LogLevel.NOTICE: "NOTICE",
            LogLevel.INFO: "INFO",
            LogLevel.DEBUG: "DEBUG",
            LogLevel.TRACE: "TRACE",
        }
        
        if self.log_to_file:
            self._setup_file_logging()
    
    def _setup_file_logging(self) -> None:
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
    def _ensure_log_file_for_today(self) -> None:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if self._log_date != today:
            if self.file_handle:
                self.file_handle.close()
                
            self._log_date = today
            log_file_path = os.path.join(self.log_dir, f"{self._log_date}.log")
            self.file_handle = open(log_file_path, "a", encoding="utf-8")
    
    def enable_file_logging(self, log_dir: str = "logs") -> None:
        self.log_to_file = True
        self.log_dir = log_dir
        self._setup_file_logging()
        
    def disable_file_logging(self) -> None:
        self.log_to_file = False
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None

    def _log(self, level: LogLevel, content: str) -> None:
        if level < self.min_level:
            return

        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        level_color = self._level_colors.get(level, "")
        level_name = self._level_names.get(level, "UNKNOWN")
        
        formatted_message = (
            f"{level_color}{timestamp}{Colors.RESET} "
            f"[{level_color}{level_name.ljust(8)}{Colors.RESET}] "
            f"{content}"
        )
        
        plain_message = f"{timestamp} [{level_name.ljust(8)}] {content}"
        
        print(formatted_message, file=self.output)
        self.output.flush()
        
        if self.log_to_file:
            self._ensure_log_file_for_today()
            if self.file_handle:
                print(plain_message, file=self.file_handle)
                self.file_handle.flush()

    def fatal(self, content: str) -> None:
        self._log(LogLevel.FATAL, content)

    def critical(self, content: str) -> None:
        self._log(LogLevel.CRITICAL, content)

    def error(self, content: str) -> None:
        self._log(LogLevel.ERROR, content)

    def warning(self, content: str) -> None:
        self._log(LogLevel.WARNING, content)

    def notice(self, content: str) -> None:
        self._log(LogLevel.NOTICE, content)

    def info(self, content: str) -> None:
        self._log(LogLevel.INFO, content)

    def debug(self, content: str) -> None:
        self._log(LogLevel.DEBUG, content)

    def trace(self, content: str) -> None:
        self._log(LogLevel.TRACE, content)
        
    def __del__(self):
        if self.file_handle:
            self.file_handle.close()


log = Logger() 