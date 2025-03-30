from telegram.ext import CommandHandler, filters, MessageHandler, Application, ConversationHandler, CallbackQueryHandler

from bot.server.interaction.registration.registration_controller import RegistrationController, StatesEnum


def init_registration_handlers(app: Application):
    registrationController = RegistrationController()

    registration_conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('register', registrationController.start_register)],
        states={
            StatesEnum.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, registrationController.input_name)],
            StatesEnum.COUNTRY: [CallbackQueryHandler(registrationController.input_country)],
            StatesEnum.CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, registrationController.input_city)],
        },
        fallbacks=[CommandHandler('cancel_register', registrationController.cancel)],
    )

    app.add_handler(registration_conversation_handler)

    print(f"Хэндлеры registration_controller зарегистрированы.")