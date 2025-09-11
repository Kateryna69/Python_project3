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


user_states = {}

async def set_commands():
    await bot.set_my_commands(ALL_BOT_COMMANDS)


# ---------- Helpers ----------
def norm(text: str) -> str:
    return text.strip().lower()


# ---------- Start / Help (commands + кнопки) ----------
@dp.message(START_COMMAND)
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привіт! Я бот для вивчення англійських слів.\n"
        "Вибери дію нижче 👇",
        reply_markup=main_kb
    )

@dp.message(lambda m: m.text and norm(m.text) in ("start", "почати", "🚀", "start"))
async def start_button(message: types.Message):
    
    await cmd_start(message)


@dp.message(HELP_COMMAND)
async def cmd_help(message: types.Message):
    await message.answer(
        "📌 Команди:\n"
        "/start – почати роботу\n"
        "/help – отримати довідку\n"
        "/addword – додати слово\n"
        "/mywords – подивитись мої слова\n"
        "/quiz – пройти тест\n"
        "/delword – видалити слово\n\n"
        "Або натисни кнопку в меню."
    )

@dp.message(lambda m: m.text and m.text.strip() == "ℹ️ Допомога")
async def help_button(message: types.Message):
    await cmd_help(message)


# ---------- Add word (command + кнопка) ----------
@dp.message(ADD_WORD_COMMAND)
async def add_word_cmd(message: types.Message):
    user_id = str(message.from_user.id)
    user_states[user_id] = {"state": "awaiting_english"}
    await message.answer("✍️ Введи слово англійською:")

@dp.message(lambda m: m.text and m.text.strip() == "➕ Додати слово")
async def add_word_btn(message: types.Message):
    await add_word_cmd(message)


# ---------- My words (command + кнопка) ----------
@dp.message(MY_WORDS_COMMAND)
async def my_words_cmd(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    words = data.get(user_id, {}).get("words", {})
    if not words:
        await message.answer("📂 У тебе ще немає слів.")
    else:
        text = "\n".join([f"{eng} — {tr}" for eng, tr in words.items()])
        await message.answer("📖 Твої слова:\n" + text)

@dp.message(lambda m: m.text and m.text.strip() == "📖 Мої слова")
async def my_words_btn(message: types.Message):
    await my_words_cmd(message)


# ---------- Delete word (command + кнопка) ----------
@dp.message(DELETE_WORD_COMMAND)
async def delete_word_cmd(message: types.Message):
    user_id = str(message.from_user.id)
    user_states[user_id] = {"state": "awaiting_delete"}
    await message.answer("Введи слово, яке хочеш видалити:")

@dp.message(lambda m: m.text and m.text.strip() == "❌ Видалити слово")
async def delete_word_btn(message: types.Message):
    await delete_word_cmd(message)


# ---------- Quiz (command + кнопка) ----------
@dp.message(QUIZ_COMMAND)
async def quiz_cmd(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    words = data.get(user_id, {}).get("words", {})
    if not words:
        await message.answer("⚠️ Спочатку додай слова для тесту.")
        return
    word, translation = random.choice(list(words.items()))
    user_states[user_id] = {"state": "awaiting_quiz", "translation": translation}
    await message.answer(f"❓ Переклади слово: {word}")

@dp.message(lambda m: m.text and m.text.strip() == "📝 Тест")
async def quiz_btn(message: types.Message):
    await quiz_cmd(message)


# ---------- Generic text handler (обробляє відповіді в станах) ----------
@dp.message()
async def handle_message(message: types.Message):
    if not message.text:
        return
    text = norm(message.text)
    
    if message.text.startswith("/"):
        return

    user_id = str(message.from_user.id)
    state = user_states.get(user_id, {}).get("state")

    if state == "awaiting_english":
        english_word = text
        data = load_data()
        if user_id not in data:
            data[user_id] = {"words": {}}
        if english_word in data[user_id]["words"]:
            await message.answer("⚠️ Це слово вже є у твоєму словнику.")
            user_states.pop(user_id, None)
            return
        user_states[user_id]["english_word"] = english_word
        user_states[user_id]["state"] = "awaiting_translation"
        await message.answer(f"✍️ Введи переклад слова '{english_word}':")
        return

    if state == "awaiting_translation":
        english_word = user_states[user_id].get("english_word")
        translation = text
        data = load_data()
        if user_id not in data:
            data[user_id] = {"words": {}}
        data[user_id]["words"][english_word] = translation
        save_data(data)
        user_states.pop(user_id, None)
        await message.answer(f"✅ Додано: {english_word} — {translation}")
        return

    if state == "awaiting_delete":
        target = text
        data = load_data()
        if user_id in data and target in data[user_id].get("words", {}):
            del data[user_id]["words"][target]
            save_data(data)
            await message.answer(f"❌ Слово '{target}' видалено.")
        else:
            await message.answer("⚠️ Такого слова немає в твоєму словнику.")
        user_states.pop(user_id, None)
        return

    if state == "awaiting_quiz":
        correct_translation = user_states[user_id].get("translation", "")
        if text == correct_translation:
            await message.answer("✅ Вірно!")
        else:
            await message.answer(f"❌ Невірно. Правильний переклад: {correct_translation}")
        user_states.pop(user_id, None)
        return

    
    return


# ---------- Запуск ----------
async def main():
    await set_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())