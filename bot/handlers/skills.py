from json import loads
from datetime import datetime, timedelta
import logging

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
import httpx


from routers.routers import user_router
from envs import API_URL, MY_API_KEY
from kb.user_kb import menu_kb, skill_edit_kb
from kb.smart_keyboard import SmartKeyboard
from filters.filters import StateFilter
from states.states import AddSkillState


assert API_URL is not None
assert MY_API_KEY is not None

@user_router.callback_query(F.data == "my_skills")
async def my_skills(cb:CallbackQuery, state:FSMContext, bot_header:dict):
    bot_header["telegram-id"] = str(cb.from_user.id)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_URL+"/skills/?only_names=true",
            headers=bot_header)
    raw = response.content
    skills:list[str] = loads(raw)
    kb = SmartKeyboard(cb.from_user)
    kb.init_keyboard()
    kb.add_buttons(skills)
    kb.set_prop([2,2,2], len(skills), next_button="➡️", back_button="⬅️", home_button="Меню")
    await state.set_state("get_skill")
    await cb.message.answer("YSP зібрав всі ваші скіли:", reply_markup=kb.get_keyboard())
    await cb.message.delete()


@user_router.callback_query(F.data == "➡️")
async def next_page(cb:CallbackQuery):
    kb = SmartKeyboard(cb.from_user)
    await cb.message.answer("YSP зібрав наступну сторінку ваших скілів:", reply_markup=kb.get_keyboard())
    await cb.message.delete()


@user_router.callback_query(F.data == "⬅️")
async def previous_page(cb:CallbackQuery):
    kb = SmartKeyboard(cb.from_user)
    await cb.message.answer("YSP переніс вас на минулу сторінку скілів:", reply_markup=kb.previous_keyboard())
    await cb.message.delete()


@user_router.callback_query(F.data == "Меню")
async def to_menu(cb:CallbackQuery, state:FSMContext):
    user = cb.from_user
    kb = SmartKeyboard(user)
    kb.delete_user(user)
    await state.clear()
    await cb.message.answer("YSP переніс вас на головну", reply_markup=menu_kb)
    await cb.message.delete()

@user_router.callback_query(F.data == "back_to_skills")
async def backto_skills(cb:CallbackQuery, state:FSMContext):
    kb = SmartKeyboard(cb.from_user)
    await cb.message.answer("YSP зібрав всі ваші скіли:", reply_markup=kb.current_keyboard())
    await cb.message.delete()

@user_router.callback_query(F.data == "increament")
async def plus_progress(cb:CallbackQuery, state:FSMContext, bot_header:dict):
    bot_header["telegram-id"] = str(cb.from_user.id)
    data = await state.get_data()
    skill:dict = data.get(cb.from_user.id)
    skill_name = skill["name"]
    async with httpx.AsyncClient() as client:
        await client.patch(
            API_URL+f"/progress/{skill_name}?add=true",
            headers=bot_header)
    await state.set_state("get_skill")
    created_at = skill["created_at"]
    total_time = skill["total_time"]
    await state.update_data({
        cb.from_user.id:{
            "name":skill_name,
            "created_at":created_at,
            "total_time":total_time + 1
                            }
                    })
    await cb.message.edit_text(
f"""Інформація по {skill_name}:
Створено: {created_at}
Прогрес: {total_time + 1}
""", reply_markup=skill_edit_kb.as_markup())
    

@user_router.callback_query(F.data == "decrement")
async def minus_progress(cb:CallbackQuery, state:FSMContext, bot_header:dict):
    bot_header["telegram-id"] = str(cb.from_user.id)
    data = await state.get_data()
    skill:dict = data.get(cb.from_user.id)
    skill_name = skill["name"]
    async with httpx.AsyncClient() as client:
        await client.patch(
            API_URL+f"/progress/{skill_name}?reduce=true",
            headers=bot_header)
    await state.set_state("get_skill")
    created_at = skill["created_at"]
    total_time = skill["total_time"]
    await state.update_data({
        cb.from_user.id:{
            "name":skill_name,
            "created_at":created_at,
            "total_time":total_time - 1
                            }
                    })
    await cb.message.edit_text(
f"""Інформація по {skill_name}:
Створено: {created_at}
Прогрес: {total_time- 1}
""", reply_markup=skill_edit_kb.as_markup())


@user_router.callback_query(F.data == "del_skill")
async def delete_skill(cb:CallbackQuery, state:FSMContext, bot_header:dict):
    bot_header["telegram-id"] = str(cb.from_user.id)
    data = await state.get_data()
    skill:dict = data.get(cb.from_user.id)
    skill_name = skill["name"]
    print(skill_name)
    async with httpx.AsyncClient() as client:
        await client.delete(
            API_URL+f"/skills/{skill_name}",
            headers=bot_header)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_URL+"/skills/?only_names=true",
            headers=bot_header)
    raw = response.content
    skills:list[str] = loads(raw)
    SmartKeyboard.delete_user(cb.from_user)
    kb = SmartKeyboard(cb.from_user)
    kb.init_keyboard()
    kb.add_buttons(skills)
    kb.set_prop([2,2,2], len(skills), next_button="➡️", back_button="⬅️", home_button="Меню")
    await cb.message.answer("Скіл видалено!", reply_markup=kb.get_keyboard())
    await cb.message.delete()


@user_router.callback_query(StateFilter("get_skill"))
async def manage_skill(cb:CallbackQuery, state:FSMContext, bot_header:dict):
    skill:str|None = cb.data
    bot_header["telegram-id"] = str(cb.from_user.id)
    async with httpx.AsyncClient() as client:
        response1 = await client.get(
            API_URL+"/progress/",
            headers=bot_header)
    progres:list[dict[str,str]] = loads(response1.content)
    for one_skill in progres:
        if one_skill["name"] == skill:
            created_at = one_skill["created_at"]
            total_time = one_skill["total_time"]
        
    created_at = (datetime.fromisoformat(created_at) + timedelta(hours=3)).strftime("%d.%m.%Y, %H:%M")
    await cb.message.answer(
f"""Інформація по {skill}:
Створено: {created_at}
Прогрес: {total_time}
""", reply_markup=skill_edit_kb.as_markup())
    await state.update_data({
        cb.from_user.id:{
            "name":skill,
            "created_at":created_at,
            "total_time":total_time
                            }
                    })
    await cb.message.delete()



@user_router.callback_query(F.data == "add_skill")
async def add_skill(cb:CallbackQuery, state:FSMContext):
    await state.set_state(AddSkillState.name)
    await cb.message.answer("Введіть назву скіла")
    await cb.message.delete()


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
async def skill_weight(message:Message, state:FSMContext, bot_header:dict):
    bot_header["telegram-id"] = str(message.from_user.id)
    weight = int(message.text)
    await state.update_data({"weight":weight})
    await message.answer("Ви додали скіл!", reply_markup=menu_kb)
    data = await state.get_data()
    await state.clear()
    async with httpx.AsyncClient() as client:
        await client.post(
            API_URL+"/skills/",
            headers=bot_header,
            json=data)


