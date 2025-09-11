from sre_parse import State
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage


from command import *
from config import BOT_TOKEN
from data import load_data, save_data
from keyboards import main_kb


class AddWordState(StatesGroup):
    english = State()
    translation = State()

class DeleteWordState(StatesGroup):
    word = State()

class QuizState(StatesGroup):
    waiting_answer = State()


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())



@dp.message(START_COMMAND)
async def start_cmd(message: types.Message):
    await message.answer("👋 Привіт! Це бот для вивчення англійських слів.\nВикористовуй меню або команди.", reply_markup=main_kb)


@dp.message(HELP_COMMAND)
async def help_cmd(message: types.Message):
    await message.answer("📚 Команди:\n"
                         "/addword – додати слово з перекладом\n"
                         "/mywords – подивитись мої слова\n"
                         "/quiz – пройти тест\n"
                         "/delword – видалити слово")


@dp.message(ADD_WORD_COMMAND)
async def add_word(message: types.Message, state: FSMContext):
    await message.answer("✍️ Введи слово англійською:")
    await state.set_state(AddWordState.english)

@dp.message(AddWordState.english, F.text)
async def save_english_word(message: types.Message, state: FSMContext):
    await state.update_data(english=message.text.lower())
    await message.answer("🔤 Тепер введи переклад:")
    await state.set_state(AddWordState.translation)

@dp.message(AddWordState.translation, F.text)
async def save_translation(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    data = load_data()
    english_word = (await state.get_data())["english"]
    translation = message.text.lower()

    if user_id not in data:
        data[user_id] = {"words": {}}

    data[user_id]["words"][english_word] = translation
    save_data(data)

    await message.answer(f"✅ Слово '{english_word}' з перекладом '{translation}' додано!")
    await state.clear()


@dp.message(MY_WORDS_COMMAND)
async def my_words(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_data()
    words = data.get(user_id, {}).get("words", {})

    if not words:
        await message.answer("📭 У тебе ще немає слів.")
        return

    text = "\n".join([f"{eng} → {ua}" for eng, ua in words.items()])
    await message.answer(f"📖 Твої слова:\n{text}")


@dp.message(QUIZ_COMMAND)
async def quiz(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    data = load_data()
    words = data.get(user_id, {}).get("words", {})

    if not words:
        await message.answer("⚠️ Спочатку додай слова для тесту.")
        return

    word, translation = random.choice(list(words.items()))
    await state.update_data(word=word, translation=translation)
    await message.answer(f"❓ Переклади слово: {word}")
    await state.set_state(QuizState.waiting_answer)

@dp.message(QuizState.waiting_answer, F.text)
async def check_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    word, translation = data["word"], data["translation"]

    if message.text.lower() == translation:
        await message.answer("✅ Вірно!")
    else:
        await message.answer(f"❌ Невірно! Правильний переклад: {translation}")

    await state.clear()


@dp.message(DELETE_WORD_COMMAND)
async def delete_word(message: types.Message, state: FSMContext):
    await message.answer("❌ Введи слово англійською, яке хочеш видалити:")
    await state.set_state(DeleteWordState.word)

@dp.message(DeleteWordState.word, F.text)
async def confirm_delete(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    data = load_data()
    word = message.text.lower()

    if word in data.get(user_id, {}).get("words", {}):
        del data[user_id]["words"][word]
        save_data(data)
        await message.answer(f"🗑️ Слово '{word}' видалено.")
    else:
        await message.answer(f"⚠️ Слово '{word}' не знайдено.")

    await state.clear()


async def main():
    await bot.set_my_commands(ALL_BOT_COMMANDS)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())