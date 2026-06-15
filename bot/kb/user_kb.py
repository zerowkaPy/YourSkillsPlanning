from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

menu_kb = InlineKeyboardMarkup(
    inline_keyboard= [[
        InlineKeyboardButton(text="Мої скіли", callback_data="my_skills"),
        InlineKeyboardButton(text="Додати скіл", callback_data="add_skill"),
        InlineKeyboardButton(text="Граф скілів", callback_data="graph")
    ]]
)

skill_edit_kb = InlineKeyboardBuilder(
    [[
        InlineKeyboardButton(text="редагувати ім'я", callback_data="name"),
        InlineKeyboardButton(text="+1 прогрес", callback_data="increament"),
        InlineKeyboardButton(text="-1 прогрес", callback_data="decrement"),
        InlineKeyboardButton(text="Видалити", callback_data="del_skill"),
        InlineKeyboardButton(text="Назад", callback_data="back_to_skills")
    ]]
)
skill_edit_kb.adjust(1,2,1,1)
