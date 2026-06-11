from dotenv import load_dotenv
import os
import logging

check_env = load_dotenv(".env")
if not check_env:
    logging.error("Environment variables weren't imported")

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")