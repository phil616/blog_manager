import os
import sys
from loguru import logger as _logger

_logger.remove()  # remove default logger

# config dir
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

format_str = "{time:YYYY-MM-DD HH:mm:ss} - app logger.io -[{level}]- {message}"


# stream
_logger.add(
    sink=sys.stdout,
    level="DEBUG",
    format=format_str,
    colorize=True,  # colorful output
)

# config file logger -- to file
_logger.add(
    format=format_str,  # format
    sink=os.path.join(log_dir, "{time:YYYY-MM-DD}.log"),  # path, filename record by day
    level="INFO",  # least level to record
    rotation="1 week",  # rotate file every week
    compression="zip",  # compress rotated file
    enqueue=True,  # async write to file
    encoding="utf-8",  # encoding of log file
    retention="30 days",  # keep log file for 30 days
    serialize=False,  # serialize record object to string
    backtrace=True,  # record traceback info
    diagnose=True,  # record system info
    catch=True,  # auto catch exception and record it
)

log = _logger
