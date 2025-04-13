from telegram.ext import Application, PicklePersistence
from telegram import BotCommand, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

from bot.config import get_settings
from bot.server import init_handlers


class TRGBot:
    def __init__(self, token: str):
        self.token = token

    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
"""Все основные возможности предоставлены в виде кнопок в меню.\n
Если вы хотите узнать больше о боте, воспользуйтесь /about""")

    @staticmethod
    async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
"""🤖 Я TRG бот и предназначен для поиска и управления сессиями для настольных ролевых игр. 🎲\n
Умею помогать игрокам находить мастеров и организовывать игры в удобном формате! 🧙‍♂️🗺️""")

    @staticmethod
    async def set_commands(app: Application) -> None:
        commands = [
        BotCommand("start", "Начать"),
        BotCommand("help", "Помощь"),
        BotCommand("about", "О боте")
    ]
        await app.bot.set_my_commands(commands)

    def build_bot(self):
        persistence = PicklePersistence(filepath=get_settings().persistence_data)
        app = Application.builder().token(self.token).persistence(persistence).build()
        return app

    @staticmethod
    def start_bot(app: Application) -> None:
        print("Бот запущен...")
        app.add_handler(CommandHandler("help", TRGBot.help_command))
        app.add_handler(CommandHandler("about", TRGBot.about))
        app.post_init = TRGBot.set_commands
        app.run_polling()
