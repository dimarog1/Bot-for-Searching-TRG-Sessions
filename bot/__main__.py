from bot import get_settings, TRGBot, init_handlers

if __name__ == '__main__':
    settings = get_settings()
    trg_bot = TRGBot(settings.BOT_TOKEN)
    app = trg_bot.build_bot()
    init_handlers(app)
    trg_bot.start_bot(app)
