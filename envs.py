import os
import logging

from dotenv import load_dotenv

check_env = load_dotenv(".env")
if not check_env:
    logging.error("Environment variables weren't imported")

DB_URL = os.getenv("DB_URL")