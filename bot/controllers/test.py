from sqlalchemy import select, func
from telegram import Update
from telegram.ext import ContextTypes

from bot.db.connection import get_session
from bot.db.models import User


class TestController:
    @staticmethod
    async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Привет! Я бот для поиска TRG сессий.")

    @staticmethod
    async def msg_echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        await update.message.reply_text(f'Вы написали: {user_message}')

    @staticmethod
    async def cmd_check_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = select(func.now())
        async for session in get_session():
            result = await session.execute(query)
            message = result.scalar_one()
            await update.message.reply_text(message)

    @staticmethod
    async def cmd_add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        new_user = User(name="aboba", age=20)
        async for session in get_session():
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  # Обновляет объект после сохранения
            await update.message.reply_text(new_user.__repr__())

    @staticmethod
    async def cmd_get_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = select(User)
        async for session in get_session():
            result = await session.execute(query)
            message = result.scalar_one()
            await update.message.reply_text(str(message))
