from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Додати слово")],
        [KeyboardButton(text="📖 Мої слова")],
        [KeyboardButton(text="📝 Тест")],
        [KeyboardButton(text="❌ Видалити слово")],
        [KeyboardButton(text="ℹ️ Допомога")],
    ],
    resize_keyboard=True
)