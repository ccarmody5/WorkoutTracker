"""
Set-up file to configure a specific logger and allow for multiple logs
"""

import logging
import os
from logging import FileHandler
from logging import Formatter

APP_LOG_FORMAT = ("%(asctime)s - %(module)-10s %(funcName)-16s %(lineno)-4s %(levelname)-7s " + ' -- ' + '%(message)s')

LOG_LEVEL = logging.INFO


def get_logs_directory_path():
    """Return the absolute path to the Logs directory in the parent directory."""
    return os.path.abspath(os.path.join(os.curdir, "logs"))


# Usage
logs_directory = get_logs_directory_path()

APP_LOG_FILE = logs_directory + "/app.log"
app_logger = logging.getLogger("app.main")
app_logger.setLevel(LOG_LEVEL)
app_logger_file_handler = FileHandler(APP_LOG_FILE)
app_logger_file_handler.setLevel(LOG_LEVEL)
app_logger_file_handler.setFormatter(Formatter(APP_LOG_FORMAT))
app_logger.addHandler(app_logger_file_handler)
