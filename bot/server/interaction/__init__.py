from telegram.ext import Application

from bot.server.interaction.start_chat import init_start_handlers
from bot.server.interaction.registration import init_registration_handlers
from bot.server.interaction.menu import init_menu_handlers


def init_handlers(app: Application):
    init_start_handlers(app)
    init_registration_handlers(app)
    init_menu_handlers(app)


__all__ = [
    init_handlers
]
