from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚 Додати слово"), KeyboardButton(text="📝 Мої слова")],
        [KeyboardButton(text="❌ Видалити слово"), KeyboardButton(text="🎯 Тест")],
        [KeyboardButton(text="ℹ️ Допомога")]
    ],
    resize_keyboard=True
)