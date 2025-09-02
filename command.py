from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand


START_COMMAND = Command("start")
HELP_COMMAND = Command("help")
ADD_WORD_COMMAND = Command("add")
WORDS_COMMAND = Command("words")
DELETE_WORD_COMMAND = Command("delete")
TEST_COMMAND = Command("test")


START_BOT_COMMAND = BotCommand(command="start", description="Запустити бота")
HELP_BOT_COMMAND = BotCommand(command="help", description="Список команд")
ADD_WORD_BOT_COMMAND = BotCommand(command="add", description="Додати слово")
WORDS_BOT_COMMAND = BotCommand(command="words", description="Показати мої слова")
DELETE_WORD_BOT_COMMAND = BotCommand(command="delete", description="Видалити слово")
TEST_BOT_COMMAND = BotCommand(command="test", description="Пройти тест")