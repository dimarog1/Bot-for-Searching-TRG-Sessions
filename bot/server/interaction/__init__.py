from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.server.interaction.conversation_states import ConversationStates
from bot.server.interaction.menu import MenuController, MenuStatesEnum
from bot.server.interaction.profile import ProfileController
from bot.server.interaction.registration import RegistrationController
from bot.server.interaction.registration.registration_service import RegistrationService
from bot.server.interaction.sessions import SessionController


def init_handlers(app: Application):
    menu_controller = MenuController()
    registration_controller = RegistrationController(menu_controller=menu_controller)
    profile_controller = ProfileController(menu_controller=menu_controller)
    session_controller = SessionController()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", registration_controller.start_register)],
        states={
            ConversationStates.ENTER_PROFILE_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, registration_controller.input_name
                )
            ],
            ConversationStates.ENTER_PROFILE_COUNTRY: [
                CallbackQueryHandler(registration_controller.input_country)
            ],
            ConversationStates.ENTER_PROFILE_CITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, registration_controller.input_city
                )
            ],
            ConversationStates.EDIT_PROFILE_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    profile_controller.edit_profile_name,
                )
            ],
            ConversationStates.EDIT_PROFILE_CITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    profile_controller.edit_profile_city,
                )
            ],
            ConversationStates.EDIT_PROFILE_COUNTRY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    profile_controller.edit_profile_country,
                )
            ],
            ConversationStates.GAME_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, session_controller.input_game_name
                )
            ],
            ConversationStates.IS_ONLINE: [
                CallbackQueryHandler(session_controller.input_is_online)
            ],
            ConversationStates.COUNTRY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, session_controller.input_country
                )
            ],
            ConversationStates.CITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, session_controller.input_city
                )
            ],
            ConversationStates.MAX_PLAYERS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    session_controller.input_max_players,
                )
            ],
            ConversationStates.START_DATE: [
                CallbackQueryHandler(session_controller.input_start_date)
            ],
            ConversationStates.START_TIME: [
                CallbackQueryHandler(session_controller.input_start_time)
            ],
            ConversationStates.DURATION_HOURS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    session_controller.input_duration_hours,
                )
            ],
            ConversationStates.MENU: [
                MessageHandler(
                    filters.TEXT
                    & ~filters.COMMAND
                    & menu_controller.regex_for_main_menu_listener,
                    menu_controller.main_menu,
                ),
                CallbackQueryHandler(
                    profile_controller.handle_edit_profile_inline_buttons,
                    pattern=r"^profile:",
                ),
                CallbackQueryHandler(
                    menu_controller.handle_sessions_inline_buttons,
                    pattern=r"^sessions:",
                ),
            ],
        },
        fallbacks=[CommandHandler("cancel", registration_controller.cancel)],
        name="main_conversation",
        persistent=True,
    )

    app.add_handler(conversation_handler)


__all__ = [
    "init_handlers",
]
