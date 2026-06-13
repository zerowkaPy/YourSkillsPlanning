from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import F
import httpx
from json import loads
from graphviz import Digraph
from pathlib import Path
from aiogram.types import BufferedInputFile

from routers import user_router
from envs import API_URL
from kb import menu_kb
from smart_keyboard import SmartKeyboard

@user_router.callback_query(F.data == "graph")
async def build_relations(cb:CallbackQuery):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(API_URL+"/skills/graph")
    relations:list[tuple[str,str]] = response.json()
    print(relations)
    graph = Digraph()
    for relate in relations:
        graph.edge(relate["parent"], relate["child"])

    png_bytes = graph.pipe(format="png")

    photo = BufferedInputFile(
        png_bytes,
        filename="skills.png"
    )
    await cb.message.answer_photo(photo)