from telegram.ext import CallbackQueryHandler, filters, Application, MessageHandler

from .menu_controller import MenuController, MenuStatesEnum


class ProfileEditFilter(filters.BaseFilter):
    def filter(self, message):
        context = message.bot.get_context(message)
        return context.user_data.get('state') in [
            MenuStatesEnum.EDIT_NAME,
            MenuStatesEnum.EDIT_CITY,
            MenuStatesEnum.EDIT_COUNTRY
        ]


def init_menu_handlers(app: Application):
    menu_controller = MenuController()

    regex_for_main_menu_listener = filters.Regex(
        f"^({MenuStatesEnum.MENU.value}|"
        f"{MenuStatesEnum.PROFILE.value}|"
        f"{MenuStatesEnum.SESSIONS.value}|"
        f"{MenuStatesEnum.MASTER_SEARCH.value}|"
        f"{MenuStatesEnum.SETTINGS.value}|"
        f"{MenuStatesEnum.SUPPORT.value})$"
    )
    app.add_handler(MessageHandler(
        filters.TEXT
        & regex_for_main_menu_listener,
        menu_controller.main_menu
    ))

    app.add_handler(CallbackQueryHandler(menu_controller.handle_inline_buttons))

    app.add_handler(MessageHandler(
        filters.TEXT
        & ~filters.COMMAND
        & ProfileEditFilter(),
        menu_controller.handle_user_response
    ))

    print(f"Хэндлеры menu_controller зарегистрированы.")
