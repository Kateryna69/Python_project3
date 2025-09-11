import asyncio
import random
import logging
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN
from data import load_data, save_data
from keyboards import main_kb
from command import (
    START_COMMAND, HELP_COMMAND, ADD_WORD_COMMAND,
    MY_WORDS_COMMAND, QUIZ_COMMAND, DELETE_WORD_COMMAND,
    ALL_BOT_COMMANDS
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_states = {}  # для станів користувача: додавання слова, тест

# ================= Команди меню =================
async def set_commands():
    await bot.set_my_commands(ALL_BOT_COMMANDS)

# ================= Хендлери =================

@dp.message(START_COMMAND)
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привіт! Я бот для вивчення англійських слів.\n"
        "Вибери дію нижче 👇",
        reply_markup=main_kb
    )

@dp.message(HELP_COMMAND)
async def cmd_help(message: types.Message):
    await message.answer(
        "📌 Команди:\n"
        "/start – почати роботу\n"
        "/help – отримати довідку\n"
        "/addword – додати слово\n"
        "/mywords – подивитись мої слова\n"
        "/quiz – пройти тест\n"
        "/delword – видалити слово"
    )

# ================= Додавання слова =================
@dp.message(ADD_WORD_COMMAND)
async def add_word(message: types.Message):
    user_id = str(message.from_user.id)
    user_states[user_id] = {"state": "awaiting_english"}
    await message.answer("✍️ Введи слово англійською:")

@dp.message()
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    state = user_states.get(user_id, {}).get("state")

    # ---------------- Додавання слова ----------------
    if state == "awaiting_english":
        english_word = message.text.lower()
        if user_id not in data:
            data[user_id] = {"words": {}}
        if english_word in data[user_id]["words"]:
            await message.answer("⚠️ Це слово вже є.")
            return
        user_states[user_id]["english_word"] = english_word
        user_states[user_id]["state"] = "awaiting_translation"
        await message.answer(f"✍️ Введи переклад слова '{english_word}':")
        return

    if state == "awaiting_translation":
        english_word = user_states[user_id]["english_word"]
        translation = message.text.lower()
        data[user_id]["words"][english_word] = translation
        save_data(data)
        user_states.pop(user_id)
        await message.answer(f"✅ Додано слово '{english_word}' з перекладом '{translation}'")
        return

    # ---------------- Видалення слова ----------------
    if state == "awaiting_delete":
        word_to_delete = message.text.lower()
        if user_id in data and word_to_delete in data[user_id]["words"]:
            del data[user_id]["words"][word_to_delete]
            save_data(data)
            await message.answer(f"❌ Слово '{word_to_delete}' видалено.")
        else:
            await message.answer("⚠️ Такого слова немає.")
        user_states.pop(user_id)
        return

    # ---------------- Тестування ----------------
    if state == "awaiting_quiz":
        correct_translation = user_states[user_id]["translation"]
        if message.text.lower() == correct_translation:
            await message.answer("✅ Вірно!")
        else:
            await message.answer(f"❌ Невірно! Правильний переклад: {correct_translation}")
        user_states.pop(user_id)
        return

# ================= Мої слова =================
@dp.message(MY_WORDS_COMMAND)
async def my_words(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    words = data.get(user_id, {}).get("words", {})
    if not words:
        await message.answer("📂 У тебе ще немає слів.")
    else:
        text = "\n".join([f"{eng} – {tr}" for eng, tr in words.items()])
        await message.answer("📖 Твої слова:\n" + text)

# ================= Видалення слова =================
@dp.message(DELETE_WORD_COMMAND)
async def delete_word(message: types.Message):
    user_id = str(message.from_user.id)
    user_states[user_id] = {"state": "awaiting_delete"}
    await message.answer("Введи слово, яке хочеш видалити:")

# ================= Тестування =================
@dp.message(QUIZ_COMMAND)
async def quiz(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    words = data.get(user_id, {}).get("words", {})
    if not words:
        await message.answer("⚠️ Спочатку додай слова для тесту.")
        return
    word, translation = random.choice(list(words.items()))
    user_states[user_id] = {"state": "awaiting_quiz", "translation": translation}
    await message.answer(f"❓ Переклади слово: {word}")



async def main():
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())