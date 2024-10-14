"""
Set-up file to configure a specific logger and allow for multiple logs
"""

import logging
import os
from logging import FileHandler
from logging import Formatter

WEBAPP_LOG_FORMAT = (
        "%(asctime)s - %(module)-10s %(funcName)-20s %(lineno)-4s %(levelname)-7s " + ' -- ' + '%(message)s')

LOG_LEVEL = logging.INFO

def get_logs_directory_path():
    """Return the absolute path to the Logs directory in the parent directory."""
    return os.path.abspath(os.path.join(os.curdir, "logs"))

# Usage
logs_directory = get_logs_directory_path()

WEBAPP_LOG_FILE = logs_directory + "/webapp.log"
webapp_logger = logging.getLogger("app.webapp")
webapp_logger.setLevel(LOG_LEVEL)
webapp_logger_file_handler = FileHandler(WEBAPP_LOG_FILE)
webapp_logger_file_handler.setLevel(LOG_LEVEL)
webapp_logger_file_handler.setFormatter(Formatter(WEBAPP_LOG_FORMAT))
webapp_logger.addHandler(webapp_logger_file_handler)
