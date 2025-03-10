# Logger

A logging system with colored output and multiple severity levels.

## Getting Started

### Installation from GitHub

```bash
# Clone the repository
git clone https://github.com/smartswap-org/logger
cd logger

# Install the package in development mode
pip install -e .
```

### Usage in Your Project

```python
from logger import log, LogLevel, Logger

# Basic logging
log.info("Regular operational message")
log.error("Runtime error occurred")

# All available log levels
log.fatal("System is unusable")
log.critical("Component failure")
log.error("Runtime error")
log.warning("Degraded performance")
log.notice("Important business event")
log.info("Regular operational message")
log.debug("Detailed flow information")
log.trace("Most granular information")

# Change minimum log level
log.min_level = LogLevel.DEBUG  # Show debug messages and above
log.min_level = LogLevel.TRACE  # Show all messages
log.min_level = LogLevel.ERROR  # Show only error and above

# Create a custom logger
custom_log = Logger(min_level=LogLevel.DEBUG)
custom_log.debug("This will be visible")

# File logging
log.enable_file_logging()  # Logs to logs/YYYY-MM-DD.log
log.info("This message will be saved to file")

# Custom log directory
log.enable_file_logging(log_dir="custom_logs")

# Disable file logging
log.disable_file_logging()

# Initialize with file logging enabled
file_logger = Logger(min_level=LogLevel.INFO, log_to_file=True, log_dir="app_logs")
```

## Running Tests

The logger comes with a comprehensive test suite to ensure all functionality works correctly.

```bash
# Run all tests
python run_tests.py

# Run tests with unittest directly
python -m unittest discover tests
```

The tests verify:
- All log levels work correctly
- Log level filtering functions properly
- Timestamp formatting is correct
- Custom loggers work as expected
- File logging functionality works
- Daily log rotation works correctly

## Running Demos

The package includes a demo script that showcases all the logger's features.

```bash
# Run the demo
python demo.py
```

The demo demonstrates:
- All log levels and their colored output
- Changing the minimum log level
- File logging functionality
- Daily log rotation (simulated)

## License

MIT 