import enum

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes, filters

from bot.server.interaction.conversation_states import ConversationStates
from bot.server.interaction.profile import ProfileController


class MenuStatesEnum(enum.Enum):
    MENU = "Меню"
    PROFILE = "Профиль"
    SESSIONS = "Сессии"
    MASTER_SEARCH = "Поиск мастеров"
    SETTINGS = "Настройки"
    SUPPORT = "Помощь"


class MenuController:
    regex_for_main_menu_listener = filters.Regex(
        f"^({MenuStatesEnum.MENU.value}|"
        f"{MenuStatesEnum.PROFILE.value}|"
        f"{MenuStatesEnum.SESSIONS.value}|"
        f"{MenuStatesEnum.MASTER_SEARCH.value}|"
        f"{MenuStatesEnum.SETTINGS.value}|"
        f"{MenuStatesEnum.SUPPORT.value})$"
    )

    @staticmethod
    async def show_main_menu(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        message="Вам доступно меню",
    ):
        keyboard = [
            [
                MenuStatesEnum.PROFILE.value,
                MenuStatesEnum.SESSIONS.value,
                MenuStatesEnum.MASTER_SEARCH.value,
                MenuStatesEnum.SETTINGS.value,
            ],
            [MenuStatesEnum.SUPPORT.value],
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True, one_time_keyboard=False
        )

        await update.message.reply_text(message, reply_markup=reply_markup)

    @staticmethod
    async def main_menu(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        text = update.message.text

        match text:
            case MenuStatesEnum.PROFILE.value:
                await ProfileController.profile(update, context)
            case MenuStatesEnum.SESSIONS.value:
                await MenuController.sessions(update, context)
            case MenuStatesEnum.MASTER_SEARCH.value:
                raise NotImplementedError(
                    f"{MenuStatesEnum.MASTER_SEARCH.value} not implemented yet"
                )
            case MenuStatesEnum.SETTINGS.value:
                raise NotImplementedError(
                    f"{MenuStatesEnum.SETTINGS.value} not implemented yet"
                )
            case MenuStatesEnum.SUPPORT.value:
                await MenuController.support(update, context)

        return ConversationStates.MENU

    @staticmethod
    async def sessions(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Мои сессии (мастер)", callback_data="sessions:my_master_sessions"
                )
            ],
            [
                InlineKeyboardButton(
                    "Мои сессии (игрок)", callback_data="sessions:my_player_sessions"
                )
            ],
            [InlineKeyboardButton("Поиск", callback_data="sessions:find_sessions")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    @staticmethod
    async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "По всем вопросам по боту обращайтесь к Дмитрию (@dimarog1) или Антону (@mureann)"
        )
        return ConversationStates.MENU

    @staticmethod
    async def handle_sessions_inline_buttons(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        query = update.callback_query
        await query.answer()

        match query.data:
            case "sessions:my_master_sessions":
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "Создать новую сессию",
                            callback_data="sessions:my_master_active_sessions_management_create",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Активные сессии",
                            callback_data="sessions:my_master_active_sessions",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Законченные сессии",
                            callback_data="sessions:my_master_ended_sessions",
                        )
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_reply_markup(reply_markup=reply_markup)
            case "sessions:my_master_active_sessions":
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "Изменить / Удалить",
                            callback_data="sessions:my_master_active_sessions_management_edit",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Показать все сессии",
                            callback_data="sessions:my_master_active_sessions_all",
                        )
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_reply_markup(reply_markup=reply_markup)
            case "sessions:my_master_active_sessions_management_edit":
                raise NotImplementedError("Editing sessions not implemented yet")
            case "sessions:my_master_active_sessions_management_create":
                await query.message.reply_text("Во что будем играть?")
                return ConversationStates.GAME_NAME
            case _:
                await query.message.reply_text("Неизвестная команда.")
                return ConversationStates.MENU

        return ConversationStates.MENU

    @staticmethod
    async def support(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        await update.message.reply_text("Напишите нам: @dimarog1 или @mureann")
        return ConversationStates.MENU
