from aiogram.filters import Command
from aiogram.types import BotCommand

# Команди для хендлерів
START_COMMAND = Command("start")
HELP_COMMAND = Command("help")
ADD_WORD_COMMAND = Command("addword")
MY_WORDS_COMMAND = Command("mywords")
QUIZ_COMMAND = Command("quiz")
DELETE_WORD_COMMAND = Command("delword")

# Команди для меню Telegram
ALL_BOT_COMMANDS = [
    BotCommand(command="start", description="Запустити бота"),
    BotCommand(command="help", description="Отримати довідку"),
    BotCommand(command="addword", description="Додати слово"),
    BotCommand(command="mywords", description="Подивитись мої слова"),
    BotCommand(command="quiz", description="Пройти тест"),
    BotCommand(command="delword", description="Видалити слово"),
]