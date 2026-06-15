import asyncio 
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import httpx

from envs import BOT_TOKEN, API_URL, MY_API_KEY
from routers.routers import user_router
from kb.user_kb import menu_kb
from kb.smart_keyboard import SmartKeyboard
import handlers.skills as skills
import handlers.relations as relations
from greeting import TEXT



dp = Dispatcher()
dp.include_router(user_router)

header = {"x-api-key":MY_API_KEY}
dp["bot_header"] = header

@dp.message(CommandStart())
async def start(message: Message, command:CommandObject):
    user_id = message.from_user.id
    headers = {"x-api-key":MY_API_KEY}
    async with httpx.AsyncClient() as client:
        auth_response = await client.post(
            API_URL+f"/login/bot/check{user_id}",
            headers=headers
            )
    if auth_response.json():
        await message.reply(TEXT, reply_markup=menu_kb)
        return
    
    token = command.args
    if token is None:
        await message.answer("Вам потрібно зареєструватися в нашому додатку!")
        return
    headers = {"x-api-key":MY_API_KEY}
    json = {
        "token":token,
        "telegram_id":user_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL+"/login/bot/confirm",
            headers=headers,
            json=json
            )
    result:str|dict[str, str] = response.json()
    if result != "Confirmed":
        if result["detail"] == "Link does not exist or link is expired":
            await message.answer("Термін дії вашого токена закінчився")
        elif result["detail"] == "Link already used":
            await message.answer("Токен вже був використаний")
    else:
        await message.reply(TEXT, reply_markup=menu_kb)


bot = Bot(BOT_TOKEN) # type: ignore

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

asyncio.run(main())