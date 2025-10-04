import sys
from typing import TextIO, Optional, Dict

from .levels import LogLevel
from .formatter import Formatter
from .file_handler import FileHandler
from .api_handler import APIHandler


class Logger:
    def __init__(self, output: TextIO = sys.stdout, min_level: LogLevel = LogLevel.INFO, log_to_file: bool = False, log_dir: str = "logs", log_to_api: bool = False, service_name: str = "qtb"):
        self.output = output
        self.min_level = min_level
        self.log_to_file = log_to_file
        self.log_to_api = log_to_api
        self.formatter = Formatter()
        self.file_handler = None
        self.api_handler = None
        
        if self.log_to_file:
            self.file_handler = FileHandler(log_dir=log_dir)
            self.file_handler.setup()
        
        if self.log_to_api:
            self.api_handler = APIHandler(service_name=service_name)
    
    def enable_file_logging(self, log_dir: str = "logs") -> None:
        self.log_to_file = True
        self.file_handler = FileHandler(log_dir=log_dir)
        self.file_handler.setup()
        
    def disable_file_logging(self) -> None:
        self.log_to_file = False
        if self.file_handler:
            self.file_handler.close()
            self.file_handler = None
    
    def enable_api_logging(self, service_name: str = "qtb") -> None:
        self.log_to_api = True
        self.api_handler = APIHandler(service_name=service_name)
        
    def disable_api_logging(self) -> None:
        self.log_to_api = False
        self.api_handler = None

    def _log(self, level: LogLevel, content: str, data: Optional[Dict[str, str]] = None) -> None:
        if level < self.min_level:
            return

        formatted_message = self.formatter.format_colored(level, content)
        print(formatted_message, file=self.output)
        self.output.flush()
        
        if self.log_to_file and self.file_handler:
            plain_message = self.formatter.format_plain(level, content)
            self.file_handler.write(plain_message)
        
        if self.log_to_api and self.api_handler:
            self.api_handler.send_log(level, content, data)

    def fatal(self, content: str, data: Optional[Dict[str, str]] = None) -> None:
        self._log(LogLevel.FATAL, content, data)

    def critical(self, content: str, data: Optional[Dict[str, str]] = None) -> None:
        self._log(LogLevel.CRITICAL, content, data)

    def error(self, content: str, data: Optional[Dict[str, str]] = None) -> None:
        self._log(LogLevel.ERROR, content, data)

    def warning(self, content: str, data: Optional[Dict[str, str]] = None) -> None:
        self._log(LogLevel.WARNING, content, data)

    def notice(self, content: str, data: Optional[Dict[str, str]] = None) -> None:
        self._log(LogLevel.NOTICE, content, data)

    def info(self, content: str, data: Optional[Dict[str, str]] = None) -> None:
        self._log(LogLevel.INFO, content, data)

    def debug(self, content: str, data: Optional[Dict[str, str]] = None) -> None:
        self._log(LogLevel.DEBUG, content, data)

    def trace(self, content: str, data: Optional[Dict[str, str]] = None) -> None:
        self._log(LogLevel.TRACE, content, data)
    
    def logAPI(self, level: LogLevel, message: str, data: Optional[Dict[str, str]] = None) -> bool:
        if not self.log_to_api or not self.api_handler:
            return False
        return self.api_handler.send_log(level, message, data)
        
    def __del__(self):
        if self.file_handler:
            self.file_handler.close()


log = Logger() 