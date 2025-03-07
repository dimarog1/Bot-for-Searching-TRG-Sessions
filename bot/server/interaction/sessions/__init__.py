from telegram.ext import CommandHandler, filters, MessageHandler, Application, ConversationHandler, CallbackQueryHandler

from bot.server.interaction.sessions.session_controller import SessionController, StatesEnum


def init_session_handlers(app: Application):
    sessionController = SessionController()

    session_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('create_session', sessionController.start_session_creation)],
        states={
            StatesEnum.GAME_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, sessionController.input_game_name)],
            StatesEnum.IS_ONLINE: [CallbackQueryHandler(sessionController.input_is_online)],
            StatesEnum.COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, sessionController.input_country)],
            StatesEnum.CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, sessionController.input_city)],
            StatesEnum.MAX_PLAYERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, sessionController.input_max_players)],
            StatesEnum.START_DATETIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, sessionController.input_start_datetime)],
            StatesEnum.DURATION_HOURS: [MessageHandler(filters.TEXT & ~filters.COMMAND, sessionController.input_duration_hours)],
        },
        fallbacks=[CommandHandler('cancel_session_creation', sessionController.cancel)],
    )

    app.add_handler(session_conversation_handler)

    print(f"Хэндлеры session_controller зарегистрированы.")
