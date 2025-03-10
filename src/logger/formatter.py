import datetime
from .levels import LogLevel
from .colors import Colors


class Formatter:
    def __init__(self):
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
    
    def format_colored(self, level: LogLevel, content: str) -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        level_color = self._level_colors.get(level, "")
        level_name = self._level_names.get(level, "UNKNOWN")
        
        return (
            f"{level_color}{timestamp}{Colors.RESET} "
            f"[{level_color}{level_name.ljust(8)}{Colors.RESET}] "
            f"{content}"
        )
    
    def format_plain(self, level: LogLevel, content: str) -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        
        level_name = self._level_names.get(level, "UNKNOWN")
        
        return f"{timestamp} [{level_name.ljust(8)}] {content}" 