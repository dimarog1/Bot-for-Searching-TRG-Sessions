import os
from .bot import TRGBot

TOKEN = os.getenv("BOT_TOKEN")
trg_bot = TRGBot(TOKEN)
