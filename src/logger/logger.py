import sys
from typing import TextIO, Optional

from .levels import LogLevel
from .formatter import Formatter
from .file_handler import FileHandler


class Logger:
    def __init__(self, output: TextIO = sys.stdout, min_level: LogLevel = LogLevel.INFO, log_to_file: bool = False, log_dir: str = "logs"):
        self.output = output
        self.min_level = min_level
        self.log_to_file = log_to_file
        self.formatter = Formatter()
        self.file_handler = None
        
        if self.log_to_file:
            self.file_handler = FileHandler(log_dir=log_dir)
            self.file_handler.setup()
    
    def enable_file_logging(self, log_dir: str = "logs") -> None:
        self.log_to_file = True
        self.file_handler = FileHandler(log_dir=log_dir)
        self.file_handler.setup()
        
    def disable_file_logging(self) -> None:
        self.log_to_file = False
        if self.file_handler:
            self.file_handler.close()
            self.file_handler = None

    def _log(self, level: LogLevel, content: str) -> None:
        if level < self.min_level:
            return

        formatted_message = self.formatter.format_colored(level, content)
        print(formatted_message, file=self.output)
        self.output.flush()
        
        if self.log_to_file and self.file_handler:
            plain_message = self.formatter.format_plain(level, content)
            self.file_handler.write(plain_message)

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
        if self.file_handler:
            self.file_handler.close()


log = Logger() 