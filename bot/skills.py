from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
import httpx
from json import loads
from datetime import datetime, timedelta

from routers import user_router
from envs import API_URL
from kb import menu_kb, skill_edit_kb
from smart_keyboard import SmartKeyboard
from filters import StateFilter
from states import AddSkillState


assert API_URL is not None

@user_router.callback_query(F.data == "my_skills")
async def my_skills(cb:CallbackQuery, state:FSMContext):
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL+"/skills/?only_names=true")
    raw = response.content
    skills:list[str] = loads(raw)
    kb = SmartKeyboard(cb.from_user)
    kb.init_keyboard()
    kb.add_butons(skills)
    kb.set_prop([2,2,2], 6, next_button="➡️", back_button="⬅️", home_button="Меню")
    await state.set_state("get_skill")
    await cb.message.answer("YSP зібрав всі ваші скіли:", reply_markup=kb.get_keyboard())

@user_router.callback_query(F.data == "➡️")
async def next_page(cb:CallbackQuery):
    kb = SmartKeyboard(cb.from_user)
    await cb.message.answer("YSP зібрав наступну сторінку ваших скілів:", reply_markup=kb.get_keyboard())

@user_router.callback_query(F.data == "⬅️")
async def previous_page(cb:CallbackQuery):
    kb = SmartKeyboard(cb.from_user)
    await cb.message.answer("YSP переніс вас на минулу сторінку скілів:", reply_markup=kb.previous_keyboard())

@user_router.callback_query(F.data == "Меню")
async def to_menu(cb:CallbackQuery, state:FSMContext):
    user = cb.from_user
    kb = SmartKeyboard(user)
    kb.delete_user(user)
    await state.clear()
    await cb.message.answer("YSP переніс вас на головну", reply_markup=menu_kb)
    await cb.message.delete()

@user_router.callback_query(StateFilter("get_skill"))
async def manage_skill(cb:CallbackQuery, state:FSMContext):
    skill:str|None = cb.data
    async with httpx.AsyncClient() as client:
        response1 = await client.get(API_URL+"/progress/")
    progres:list[dict[str,str]] = loads(response1.content)
    for one_skill in progres:
        if one_skill["name"] == skill:
            created_at = one_skill["created_at"]
            total_time = one_skill["total_time"]
        
    created_at = (datetime.fromisoformat(created_at) + timedelta(hours=3)).strftime("%d.%m.%Y, %H:%M")
    await state.clear()
    await cb.message.answer(
f"""Інформація по {skill}:
Створено: {created_at}
Прогрес: {total_time}
""", reply_markup=skill_edit_kb.as_markup())
    await state.set_data({"last_skill":skill})


@user_router.callback_query(F.data == "add_skill")
async def add_skill(cb:CallbackQuery, state:FSMContext):
    await state.set_state(AddSkillState.name)
    await cb.message.answer("Введіть назву скіла")

@user_router.message(StateFilter(AddSkillState.name))
async def skill_name(message:Message, state:FSMContext):
    await state.set_data({"name":message.text})
    await state.set_state(AddSkillState.desc)
    await message.answer("Введіть опис вашого скіла(яка ваша ціль, якого рівня скіла ви хочете досягнути і т.д)")

@user_router.message(StateFilter(AddSkillState.desc))
async def skill_desc(message:Message, state:FSMContext):
    await state.update_data({"desc":message.text})
    await state.set_state(AddSkillState.weight)
    await message.answer("Введіть цифру від 0 до 5, на скільки для вас цей скіл важливий")

@user_router.message(StateFilter(AddSkillState.weight))
async def skill_weight(message:Message, state:FSMContext):
    weight = int(message.text)
    await state.update_data({"weight":weight})
    await message.answer("Ви додали скіл!", reply_markup=menu_kb)
    data = await state.get_data()
    await state.clear()
    print(data)
    print(type(data))
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL+"/skills/", json=data)

@user_router.callback_query(F.data == "del_skill")
async def delete_skill(cb:CallbackQuery, state:FSMContext):
    data = await state.get_data()
    skill = data.get("last_skill", "null")
    async with httpx.AsyncClient() as client:
        response = await client.delete(API_URL+f"/skills/{skill}")
    await cb.message.answer("Скіл видалено!", reply_markup=menu_kb)
    