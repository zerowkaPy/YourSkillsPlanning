import os

from aiogram import Bot, Dispatcher
from bot.storage import PostgreStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
assert BOT_TOKEN is not None


dp = Dispatcher(storage=PostgreStorage())
bot = Bot(BOT_TOKEN)
