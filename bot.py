import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from command import *
from data import load_data, save_data
from models import UserData
from keyboards import main_kb


# Ініціалізація
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# Дані користувачів
users = {}
data = load_data()
for uid, udata in data.items():
    users[uid] = UserData.from_dict(uid, udata)


@dp.message(START_COMMAND)
async def cmd_start(message: types.Message):
    users[str(message.from_user.id)] = users.get(str(message.from_user.id), UserData(str(message.from_user.id)))
    await message.answer("Привіт 👋 Я бот для вивчення англійських слів!", reply_markup=main_kb)


@dp.message(HELP_COMMAND)
async def cmd_help(message: types.Message):
    await message.answer(
        "📘 Я допоможу тобі з англійською:\n"
        "/addword <слово> <переклад> – додати слово\n"
        "/mywords – показати твої слова\n"
        "/quiz – пройти тест\n"
        "/delword <слово> – видалити слово\n"
    )


@dp.message(ADD_WORD_COMMAND)
async def cmd_addword(message: types.Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("⚠ Використання: /addword <слово> <переклад>")
        return

    word, translation = args[1], args[2]
    user = users.setdefault(str(message.from_user.id), UserData(str(message.from_user.id)))
    user.add_word(word, translation)

    save_data({uid: u.to_dict() for uid, u in users.items()})
    await message.answer(f"✅ Додано слово: <b>{word}</b> – {translation}")


@dp.message(MY_WORDS_COMMAND)
async def cmd_mywords(message: types.Message):
    user = users.get(str(message.from_user.id))
    if not user or not user.words:
        await message.answer("📭 У тебе ще немає слів.")
        return

    text = "📚 Твої слова:\n"
    for w in user.words:
        text += f"• <b>{w['word']}</b> – {w['translation']}\n"
    await message.answer(text)


@dp.message(QUIZ_COMMAND)
async def cmd_quiz(message: types.Message):
    user = users.get(str(message.from_user.id))
    if not user or not user.words:
        await message.answer("📭 Немає слів для тесту.")
        return

    word = random.choice(user.words)
    await message.answer(f"❓ Як перекладається слово: <b>{word['word']}</b>?")


@dp.message(DELETE_WORD_COMMAND)
async def cmd_delword(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("⚠ Використання: /delword <слово>")
        return

    word = args[1]
    user = users.get(str(message.from_user.id))
    if not user:
        await message.answer("📭 У тебе ще немає слів.")
        return

    user.delete_word(word)
    save_data({uid: u.to_dict() for uid, u in users.items()})
    await message.answer(f"🗑 Слово <b>{word}</b> видалене.")


async def main():
    await bot.set_my_commands(ALL_BOT_COMMANDS)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())