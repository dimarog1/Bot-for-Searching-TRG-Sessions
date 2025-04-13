from telegram.ext import Application, PicklePersistence

from bot.config import get_settings
from bot.server import init_handlers


class TRGBot:
    def __init__(self, token: str):
        self.token = token

    def build_bot(self):
        persistence = PicklePersistence(filepath=get_settings().persistence_data)
        app = Application.builder().token(self.token).persistence(persistence).build()
        return app

    @staticmethod
    def start_bot(app: Application) -> None:
        print("Бот запущен")
        app.run_polling()
