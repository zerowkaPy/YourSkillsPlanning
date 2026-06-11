from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
import httpx
from json import loads

from routers import user_router
from envs import API_URL

@user_router.callback_query(F.data == "Мої скіли")
async def my_skills(cb: CallbackQuery, state: FSMContext):
    response = httpx.get(API_URL+"/skills/")
    raw = response.content
    skills:list[dict[str, str]] = loads(raw)
    await cb.message.answer(text=raw.decode())
