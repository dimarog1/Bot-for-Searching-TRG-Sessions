from telegram.ext import Application

from bot.server import init_handlers
from bot.config import get_settings


class TRGBot:
    def __init__(self, token: str):
        self.token = token

    def build_bot(self):
        app = Application.builder().token(self.token).build()
        return app

    @staticmethod
    def start_bot(app: Application) -> None:
        print("Бот запущен...")
        app.run_polling()
