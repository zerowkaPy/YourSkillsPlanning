from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_kb = InlineKeyboardMarkup(
    inline_keyboard= [[
        InlineKeyboardButton(text="Мої скіли", callback_data="Мої скіли"),
        InlineKeyboardButton(text="Граф скілів", callback_data="Граф скілів")
    ]]
)