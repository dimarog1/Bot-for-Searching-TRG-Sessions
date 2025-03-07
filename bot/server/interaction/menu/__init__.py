from telegram.ext import CallbackQueryHandler, filters, Application, MessageHandler

from .menu_controller import MenuController


def init_menu_handlers(app: Application):
    menu_controller = MenuController()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_controller.main_menu))
    app.add_handler(CallbackQueryHandler(menu_controller.handle_inline_buttons))

    print(f"Хэндлеры menu_controller зарегистрированы.")
