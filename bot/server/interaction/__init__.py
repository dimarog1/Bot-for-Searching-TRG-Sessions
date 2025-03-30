from telegram.ext import Application

from bot.server.interaction.start_chat import init_start_handlers
from bot.server.interaction.registration import init_registration_handlers
from bot.server.interaction.sessions import init_session_handlers
from bot.server.interaction.menu import init_menu_handlers


def init_handlers(app: Application):
    init_start_handlers(app)
    init_registration_handlers(app)
    init_menu_handlers(app)
    init_session_handlers(app)


__all__ = [
    init_handlers
<<<<<<< HEAD
]
=======
]
>>>>>>> 774b0492a9ba84a8ef4c260c48d65e22bcf2fdae