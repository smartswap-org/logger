import os
import datetime
from typing import Optional, TextIO


class FileHandler:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self.file_handle = None
        self._log_date = None
        
    def setup(self) -> None:
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
    def ensure_log_file_for_today(self) -> None:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if self._log_date != today:
            if self.file_handle:
                self.file_handle.close()
                
            self._log_date = today
            log_file_path = os.path.join(self.log_dir, f"{self._log_date}.log")
            self.file_handle = open(log_file_path, "a", encoding="utf-8")
    
    def write(self, message: str) -> None:
        self.ensure_log_file_for_today()
        if self.file_handle:
            print(message, file=self.file_handle)
            self.file_handle.flush()
    
    def close(self) -> None:
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None 