"""
' dbHelper.py
' 10/7/2024 - Chris Carmody
'
' This file manages db connections
"""
import sys

from environs import Env
from sqlalchemy import create_engine, URL

import config.db_log_config as log_config

logger = log_config.db_logger

logger.info("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX dbHelper.py has started XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# Used to get environment variables from .env file
env = Env()
env.read_env(".env")

def create_db_engine():
    logger.info('creating db engine')
    url = URL.create(
        drivername="postgresql+psycopg2",  # driver name = postgresql + the library we are using (psycopg2)
        username=env.str("POSTGRES_USER"),
        password=env.str("POSTGRES_PASSWORD"),
        host=env.str("POSTGRES_HOST"),
        database=env.str("POSTGRES_DB"),
        port=5432
    ).render_as_string(hide_password=False)

    # Create postgres engine
    try:
        engine = create_engine(url, echo=False)
        engine.connect()
        return engine

    except Exception as e:
        logger.error(e)
        exit_program(e)

def exit_program(e):
    print(f"Exiting due to error: {e}")
    sys.exit(1)
