# Logger

A simple logging system with colored output and daily file rotation.

## Installation

```bash
git clone https://github.com/smartswap-org/logger
cd logger
pip install -e .
```

## Basic Usage

```python
from logger import log, LogLevel

# Log messages with different severity levels
log.info("Information message")
log.error("Error message")
log.debug("Debug information")

# Set minimum log level
log.min_level = LogLevel.ERROR  # Only show ERROR and above

# Enable file logging
log.enable_file_logging()  # Logs to logs/YYYY-MM-DD.log
log.enable_file_logging(log_dir="custom_logs")  # Custom directory
log.disable_file_logging()  # Stop file logging

# Create custom logger
custom_log = Logger(min_level=LogLevel.DEBUG, log_to_file=True, log_dir="app_logs")
```

## Testing & Demo

```bash
python run_tests.py  # Run tests
python demo.py       # Run demo
```

## License

MIT 