from sqlalchemy import Update
from telegram import BotCommand, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

from bot.server import init_handlers
from bot.config import get_settings


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
        app = Application.builder().token(self.token).build()
        return app

    @staticmethod
    def start_bot(app: Application) -> None:
        print("Бот запущен...")
        app.add_handler(CommandHandler("help", TRGBot.help_command))
        app.add_handler(CommandHandler("about", TRGBot.about))
        app.post_init = TRGBot.set_commands
        app.run_polling()
