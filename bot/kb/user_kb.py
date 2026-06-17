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
        InlineKeyboardButton(text="Редагувати", callback_data="edit"),
        InlineKeyboardButton(text="+1 рівень", callback_data="increament"),
        InlineKeyboardButton(text="-1 рівень", callback_data="decrement"),
        InlineKeyboardButton(text="Видалити", callback_data="del_skill"),
        InlineKeyboardButton(text="Назад", callback_data="back_to_skills")
    ]]
)
skill_edit_kb.adjust(1,2,1,1)


edit_more_kb = InlineKeyboardBuilder(
    [[
        InlineKeyboardButton(text="Назва", callback_data="c_name"),
        InlineKeyboardButton(text="Опис", callback_data="c_desc"),
        InlineKeyboardButton(text="Важливість", callback_data="c_weight")
    ]]
)
edit_more_kb.adjust(1,1,1)




