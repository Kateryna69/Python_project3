import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import BOT_TOKEN
from command import register_commands

from aiogram import types
from aiogram.filters import Command

user_words = {}
# --- Створення бота та диспетчера ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# --- Хендлер старту ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! 👋 Я бот для вивчення англійської мови.\n"
        "Використовуй /help, щоб побачити всі команди."
    )


# --- Хендлер допомоги ---
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📚 Доступні команди:\n"
        "/add — додати слово\n"
        "/words — показати твої слова\n"
        "/delete — видалити слово\n"
        "/test — пройти тест\n"
        "/help — допомога"
    )


def register_commands(dp):
    @dp.message(Command("add"))
    async def cmd_add(message: types.Message):
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            await message.answer("❌ Напиши слово після команди /add")
            return

        word = parts[1].strip()
        user_id = message.from_user.id
        user_words.setdefault(user_id, []).append(word)

        await message.answer(f"✅ Слово <b>{word}</b> додано!", parse_mode="HTML")

    @dp.message(Command("words"))
    async def cmd_words(message: types.Message):
        user_id = message.from_user.id
        words = user_words.get(user_id, [])
        if not words:
            await message.answer("У тебе ще немає слів. Додай їх через /add")
        else:
            await message.answer("📖 Твої слова:\n" + "\n".join(words))

    @dp.message(Command("delete"))
    async def cmd_delete(message: types.Message):
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            await message.answer("❌ Напиши слово після /delete")
            return

        word = parts[1].strip()
        user_id = message.from_user.id
        words = user_words.get(user_id, [])

        if word in words:
            words.remove(word)
            await message.answer(f"🗑️ Слово <b>{word}</b> видалено!", parse_mode="HTML")
        else:
            await message.answer(f"❌ Слова <b>{word}</b> немає у твоєму списку.", parse_mode="HTML")

    @dp.message(Command("test"))
    async def cmd_test(message: types.Message):
        user_id = message.from_user.id
        words = user_words.get(user_id, [])

        if not words:
            await message.answer("У тебе немає слів для тесту. Додай їх через /add")
            return

        import random
        word = random.choice(words)
        await message.answer(
            f"❓ Як перекладається слово: <b>{word}</b> ? (Відповідь просто напиши у чат 🙂)",
            parse_mode="HTML"
        )


async def main():
    # реєструємо всі додаткові команди з command.py
    register_commands(dp)

    # встановлюємо команди в меню Telegram
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Почати роботу"),
        types.BotCommand(command="help", description="Допомога"),
        types.BotCommand(command="add", description="Додати слово"),
        types.BotCommand(command="words", description="Показати мої слова"),
        types.BotCommand(command="delete", description="Видалити слово"),
        types.BotCommand(command="test", description="Пройти тест"),
    ])

    print("✅ Бот запущений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())