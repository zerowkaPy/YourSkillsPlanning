from aiogram.filters.base import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Update

class StateFilter(Filter):
    def __init__(self, expected_state:str):
        self.expected_state = expected_state

    async def __call__(self, event:Update, state:FSMContext):
        current_state:str|None = await state.get_state()
        return self.expected_state == current_state
    