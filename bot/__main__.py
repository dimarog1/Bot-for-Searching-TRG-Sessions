from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, InlineQueryHandler

from bot.config import get_settings
from .controllers import controllers


class TRGBot:
    def __init__(self, token: str):
        self.token = token

    def start_bot(self) -> None:
        app = Application.builder().token(self.token).build()

        TRGBot.register_controllers(app)

        print("Бот запущен...")
        app.run_polling()

    @staticmethod
    def register_controllers(app: Application):
        for controller in controllers:
            for method_name in dir(controller):
                if not method_name.startswith("_"):  # Пропускаем приватные методы
                    method = getattr(controller, method_name)
                    if callable(method):
                        if method_name.startswith("cmd_"):
                            command = method_name[4:]
                            app.add_handler(CommandHandler(command, method))
                            print(f"Команда /{command} зарегистрирована.")
                        elif method_name.startswith("msg_"):
                            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, method))
                            print(f"Обработчик сообщений {method_name} зарегистрирован.")

                        elif method_name.startswith("cb_"):
                            app.add_handler(CallbackQueryHandler(method))
                            print(f"Обработчик колбэков {method_name} зарегистрирован.")

                        elif method_name.startswith("inline_"):
                            app.add_handler(InlineQueryHandler(method))
                            print(f"Обработчик инлайн-запросов {method_name} зарегистрирован.")

                        elif method_name.startswith("err_"):
                            print(f"Обработчик ошибок {method_name} зарегистрирован, но не добавлен автоматически.")


if __name__ == '__main__':
    settings = get_settings()
    trg_bot = TRGBot(settings.BOT_TOKEN)
    trg_bot.start_bot()
