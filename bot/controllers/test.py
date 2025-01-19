from sqlalchemy import select, func
from telegram import Update
from telegram.ext import ContextTypes

from db.models.user import User, Base


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
        session_factory = context.application.session_factory

        query = select(func.now())
        async with session_factory() as session:
            result = await session.execute(query)
            message = result.scalar_one()
            await update.message.reply_text(message)

    @staticmethod
    async def cmd_add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        session_factory = context.application.session_factory
        engine = session_factory.kw["bind"]

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with session_factory() as session:
            new_user = User(id=1, name="aboba", age=20)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  # Обновляет объект после сохранения
            await update.message.reply_text(new_user.__repr__())

    @staticmethod
    async def cmd_get_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        session_factory = context.application.session_factory

        query = select(User)
        async with session_factory() as session:
            result = await session.execute(query)
            message = result.scalar_one()
            await update.message.reply_text(str(message))
