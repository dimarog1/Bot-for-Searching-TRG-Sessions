from telegram.ext import CommandHandler, Application

from .start_chat_controller import StartChatController


def init_start_handlers(app: Application):
    app.add_handler(CommandHandler("start", StartChatController.command_start))

    print(f"Хэндлеры start_controller зарегистрирована.")
