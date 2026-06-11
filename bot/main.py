import asyncio 
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from envs import BOT_TOKEN
from routers import user_router
from kb import menu_kb
import skills_crud




dp = Dispatcher()
dp.include_router(user_router)


@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Вітаю", reply_markup=menu_kb)



bot = Bot(BOT_TOKEN)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

asyncio.run(main())