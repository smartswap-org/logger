# Logger

A logging system with colored output and multiple severity levels.

## Installation

```bash
pip install -e .
```

## Usage

```python
from logger import log, LogLevel

log.info("Regular operational message")
log.error("Runtime error occurred")

log.fatal("System is unusable")
log.critical("Component failure")
log.error("Runtime error")
log.warning("Degraded performance")
log.notice("Important business event")
log.info("Regular operational message")
log.debug("Detailed flow information")
log.trace("Most granular information")

log.min_level = LogLevel.DEBUG
log.min_level = LogLevel.TRACE
log.min_level = LogLevel.ERROR

custom_log = Logger(min_level=LogLevel.DEBUG)
custom_log.debug("This will be visible")

log.enable_file_logging()
log.info("This message will be saved to file")

log.enable_file_logging(log_dir="custom_logs")

log.disable_file_logging()

file_logger = Logger(min_level=LogLevel.INFO, log_to_file=True, log_dir="app_logs")
```

## License

MIT 