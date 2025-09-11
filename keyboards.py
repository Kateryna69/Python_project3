from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/addword"), KeyboardButton(text="/mywords")],
        [KeyboardButton(text="/quiz"), KeyboardButton(text="/delword")],
    ],
    resize_keyboard=True
)