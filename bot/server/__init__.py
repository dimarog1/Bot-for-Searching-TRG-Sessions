from telegram.ext import Application

from .start_chat import init_start_handlers
from .registration import init_registration_handlers


def init_handlers(app: Application):
    init_start_handlers(app)
    init_registration_handlers(app)


__all__ = [
    init_handlers
]
