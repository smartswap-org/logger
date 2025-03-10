from src.logger import log, LogLevel, Logger
import os
import time
import datetime
import shutil


def create_demo_log_files():
    demo_dir = "demo_logs_rotation"
    
    if os.path.exists(demo_dir):
        shutil.rmtree(demo_dir)
    
    os.makedirs(demo_dir)
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    today_file = os.path.join(demo_dir, f"{today}.log")
    tomorrow_file = os.path.join(demo_dir, f"{tomorrow}.log")
    
    with open(today_file, "w") as f:
        f.write(f"{today} 08:00:00 [INFO    ] Application started\n")
        f.write(f"{today} 12:30:45 [INFO    ] User logged in\n")
        f.write(f"{today} 18:15:22 [ERROR   ] Database connection timeout\n")
        f.write(f"{today} 23:59:59 [INFO    ] End of day processing\n")
    
    with open(tomorrow_file, "w") as f:
        f.write(f"{tomorrow} 00:00:01 [INFO    ] New day started\n")
        f.write(f"{tomorrow} 04:30:10 [WARNING ] Low disk space detected\n")
        f.write(f"{tomorrow} 09:15:00 [INFO    ] Daily backup completed\n")
    
    return demo_dir, today_file, tomorrow_file


def demonstrate_log_levels():
    log.fatal("This is a FATAL message")
    log.critical("This is a CRITICAL message")
    log.error("This is an ERROR message")
    log.warning("This is a WARNING message")
    log.notice("This is a NOTICE message")
    log.info("This is an INFO message")
    log.debug("This is a DEBUG message")
    log.trace("This is a TRACE message")


def demonstrate_file_logging():
    log.enable_file_logging(log_dir="demo_logs")
    log.info("This message will be saved to the demo_logs folder")
    log.error("This error message will also be saved to the demo_logs folder")
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join("demo_logs", f"{today}.log")
    print(f"Log file created at: {log_file_path}")
    
    file_logger = Logger(min_level=LogLevel.DEBUG, log_to_file=True, log_dir="demo_logs")
    file_logger.debug("Debug message from dedicated file logger")
    file_logger.info("Info message from dedicated file logger")
    
    try:
        with open(log_file_path, "r") as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading log file: {e}")


def demonstrate_log_rotation():
    demo_dir, today_file, tomorrow_file = create_demo_log_files()
    
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    tomorrow_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"In a long-running application, logs would be automatically separated by day:")
    print(f"- {today_date}.log - for logs generated on {today_date}")
    print(f"- {tomorrow_date}.log - for logs generated on {tomorrow_date}")
    
    print("\nListing created log files:")
    os.system(f"ls -la {demo_dir}")
    
    print("\nContents of today's log file:")
    with open(today_file, "r") as f:
        print(f.read())
    
    print("\nContents of tomorrow's log file:")
    with open(tomorrow_file, "r") as f:
        print(f.read())
        
    print("\nThis demonstrates how the logger automatically creates a new file each day")
    print("without requiring any intervention, as long as the application keeps running.")


if __name__ == "__main__":
    print("Demonstrating all log levels:")
    demonstrate_log_levels()
    
    print("\nChanging log level to TRACE to show all messages:")
    log.min_level = LogLevel.TRACE
    demonstrate_log_levels()
    
    print("\nDemonstrating file logging to 'demo_logs' folder:")
    demonstrate_file_logging()
    
    print("\nDemonstrating daily log rotation (simulated):")
    demonstrate_log_rotation() 