import unittest
import io
import re
import os
import shutil
import tempfile
from datetime import datetime
from src.logger import Logger, LogLevel


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        self.logger = Logger(output=self.output, min_level=LogLevel.TRACE)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if hasattr(self, 'temp_dir') and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_log_levels(self):
        self.logger.fatal("Fatal message")
        self.logger.critical("Critical message")
        self.logger.error("Error message")
        self.logger.warning("Warning message")
        self.logger.notice("Notice message")
        self.logger.info("Info message")
        self.logger.debug("Debug message")
        self.logger.trace("Trace message")
        
        output = self.output.getvalue()
        
        self.assertIn("FATAL", output)
        self.assertIn("CRITICAL", output)
        self.assertIn("ERROR", output)
        self.assertIn("WARNING", output)
        self.assertIn("NOTICE", output)
        self.assertIn("INFO", output)
        self.assertIn("DEBUG", output)
        self.assertIn("TRACE", output)
        
        self.assertIn("Fatal message", output)
        self.assertIn("Critical message", output)
        self.assertIn("Error message", output)
        self.assertIn("Warning message", output)
        self.assertIn("Notice message", output)
        self.assertIn("Info message", output)
        self.assertIn("Debug message", output)
        self.assertIn("Trace message", output)

    def test_min_level_filtering(self):
        self.logger.min_level = LogLevel.ERROR
        
        self.logger.fatal("Fatal message")
        self.logger.critical("Critical message")
        self.logger.error("Error message")
        self.logger.warning("Warning message")
        self.logger.info("Info message")
        
        output = self.output.getvalue()
        
        self.assertIn("Fatal message", output)
        self.assertIn("Critical message", output)
        self.assertIn("Error message", output)
        self.assertNotIn("Warning message", output)
        self.assertNotIn("Info message", output)

    def test_timestamp_format(self):
        self.logger.info("Test message")
        output = self.output.getvalue()
        
        current_year = str(datetime.now().year)
        self.assertIn(current_year, output)
        
        timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        self.assertTrue(re.search(timestamp_pattern, output))

    def test_custom_logger(self):
        custom_output = io.StringIO()
        custom_logger = Logger(output=custom_output, min_level=LogLevel.WARNING)
        
        custom_logger.error("Error message")
        custom_logger.warning("Warning message")
        custom_logger.info("Info message")
        
        output = custom_output.getvalue()
        
        self.assertIn("Error message", output)
        self.assertIn("Warning message", output)
        self.assertNotIn("Info message", output)
        
    def test_file_logging_enable_disable(self):
        log_dir = os.path.join(self.temp_dir, "logs")
        self.logger.enable_file_logging(log_dir=log_dir)
        
        self.logger.info("File log test")
        
        today = datetime.now().strftime("%Y-%m-%d")
        log_file_path = os.path.join(log_dir, f"{today}.log")
        
        self.assertTrue(os.path.exists(log_file_path))
        
        with open(log_file_path, "r") as f:
            content = f.read()
            self.assertIn("INFO", content)
            self.assertIn("File log test", content)
        
        self.logger.disable_file_logging()
        self.logger.info("This should not be logged to file")
        
        with open(log_file_path, "r") as f:
            content = f.read()
            self.assertNotIn("This should not be logged to file", content)
            
    def test_file_logging_constructor(self):
        log_dir = os.path.join(self.temp_dir, "constructor_logs")
        file_logger = Logger(output=self.output, min_level=LogLevel.INFO, 
                            log_to_file=True, log_dir=log_dir)
        
        file_logger.info("Constructor file log test")
        
        today = datetime.now().strftime("%Y-%m-%d")
        log_file_path = os.path.join(log_dir, f"{today}.log")
        
        self.assertTrue(os.path.exists(log_file_path))
        
        with open(log_file_path, "r") as f:
            content = f.read()
            self.assertIn("INFO", content)
            self.assertIn("Constructor file log test", content)
            
    def test_file_logging_min_level(self):
        log_dir = os.path.join(self.temp_dir, "level_logs")
        file_logger = Logger(output=self.output, min_level=LogLevel.WARNING, 
                            log_to_file=True, log_dir=log_dir)
        
        file_logger.error("Error message")
        file_logger.warning("Warning message")
        file_logger.info("Info message")
        
        today = datetime.now().strftime("%Y-%m-%d")
        log_file_path = os.path.join(log_dir, f"{today}.log")
        
        with open(log_file_path, "r") as f:
            content = f.read()
            self.assertIn("ERROR", content)
            self.assertIn("WARNING", content)
            self.assertNotIn("INFO", content)


if __name__ == "__main__":
    unittest.main() 