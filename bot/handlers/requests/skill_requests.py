from json import loads
from datetime import datetime, timedelta
import logging
from typing import Any


from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import F
import httpx
from httpx import AsyncClient


from routers.routers import user_router
from envs import API_URL, MY_API_KEY
from kb.user_kb import menu_kb, skill_edit_kb, edit_more_kb
from kb.smart_keyboard import SmartKeyboard
from filters.filters import StateFilter
from states.states import AddSkillState


assert API_URL is not None
assert MY_API_KEY is not None


async def get_names(bot_headers:dict[str, Any]|None = None) -> list[dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_URL+"/skills/?only_names=true",
            headers=bot_headers)
    skills:list[dict[str, Any]] = response.json()
    return skills


async def get_skills(client:AsyncClient, bot_headers:dict[str, Any]|None = None) -> list[dict[str, Any]]:
    response = await client.get(
        API_URL+"/skills/",
        headers=bot_headers)
    skills:list[dict[str, Any]] = response.json()
    return skills


async def get_progress(client:AsyncClient, bot_headers:dict[str, Any]|None = None) -> list[dict[str, Any]]:
    response = await client.get(
        API_URL+"/progress/",
        headers=bot_headers)
    progress:list[dict[str, Any]] = response.json()
    return progress


async def do_increament(skill_name:str|None = None, bot_headers:dict[str, Any]|None = None):
    async with httpx.AsyncClient() as client:
        await client.patch(
            API_URL+f"/progress/{skill_name}?add=true",
            headers=bot_headers)
        
async def do_decrement(skill_name:str|None = None, bot_headers:dict[str, Any]|None = None):
    async with httpx.AsyncClient() as client:
        await client.patch(
            API_URL+f"/progress/{skill_name}?reduce=true",
            headers=bot_headers)
        
async def delete_skill(skill_name:str|None = None, bot_headers:dict[str, Any]|None = None):
    async with httpx.AsyncClient() as client:
        await client.delete(
            API_URL+f"/skills/{skill_name}",
            headers=bot_headers)