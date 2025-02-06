from sqlalchemy import select, func
from telegram import Update
from telegram.ext import ContextTypes

from bot.db.connection import SessionManager
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
        try:
            query = select(func.now())
            async with SessionManager.get_session() as session:
                result = await session.execute(query)
                message = result.scalar_one()
                await update.message.reply_text(message)
        except Exception as e:
            print(e)

    @staticmethod
    async def cmd_add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            new_user = User(
                name="abobik",
                tg_id="123",
                country="Abobia",
                city="Zhopa",
                rating=1.5
            )
            async with SessionManager.get_session() as session:
                session.add(new_user)

            await update.message.reply_text(new_user.__repr__())
        except Exception as e:
            print(e)

    @staticmethod
    async def cmd_get_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            query = select(User).where(User.id_ == 1)
            async with SessionManager.get_session() as session:
                result = await session.execute(query)
                message = result.scalar_one()
            await update.message.reply_text(str(message))
        except Exception as e:
            print(e)
