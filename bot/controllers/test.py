from telegram import Update
from telegram.ext import ContextTypes


class TestController:
    @staticmethod
    async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Привет! Я бот для поиска TRG сессий.")

    @staticmethod
    async def msg_echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        await update.message.reply_text(f'Вы написали: {user_message}')
