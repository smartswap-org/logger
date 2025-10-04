import os
import requests
from typing import Optional, Dict
from threading import Thread
from queue import Queue
from .dto import LogDTO
from .levels import LogLevel


class APIHandler:
    def __init__(self, service_name: str = "qtb"):
        self.service_name = service_name
        nexus_port = os.getenv('NEXUS_PORT', '8080')
        self.nexus_url = f"http://nexus-api:{nexus_port}/logs"
        self.enabled = True
        self.log_queue = Queue()
        self._start_worker()

    def _level_to_string(self, level: LogLevel) -> str:
        level_map = {
            LogLevel.FATAL: "FATAL",
            LogLevel.CRITICAL: "CRITICAL",
            LogLevel.ERROR: "ERROR",
            LogLevel.WARNING: "WARNING",
            LogLevel.NOTICE: "NOTICE",
            LogLevel.INFO: "INFO",
            LogLevel.DEBUG: "DEBUG",
            LogLevel.TRACE: "TRACE"
        }
        return level_map.get(level, "INFO")

    def _worker(self) -> None:
        while True:
            try:
                log_dto = self.log_queue.get()
                if log_dto is None:
                    break
                requests.post(
                    self.nexus_url,
                    json=log_dto.to_dict(),
                    timeout=2
                )
            except Exception:
                pass
            finally:
                self.log_queue.task_done()

    def _start_worker(self) -> None:
        worker_thread = Thread(target=self._worker, daemon=True)
        worker_thread.start()

    def send_log(self, level: LogLevel, message: str, data: Optional[Dict[str, str]] = None) -> bool:
        if not self.enabled:
            return False

        try:
            log_dto = LogDTO(
                level=self._level_to_string(level),
                service=self.service_name,
                message=message,
                data=data or {}
            )
            self.log_queue.put_nowait(log_dto)
            return True
        except Exception:
            return False

    def disable(self) -> None:
        self.enabled = False

    def enable(self) -> None:
        self.enabled = True

