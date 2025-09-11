from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Додати слово")],
        [KeyboardButton(text="Мої слова")],
        [KeyboardButton(text="Пройти тест")],
        [KeyboardButton(text="Видалити слово")],
        [KeyboardButton(text="Допомога")],
    ],
    resize_keyboard=True
)