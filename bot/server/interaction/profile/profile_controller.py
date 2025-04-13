from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.exceptions.registration_exceptions import UserNotExistsException
from bot.server.interaction.conversation_states import ConversationStates
from bot.server.interaction.profile.profile_service import ProfileService


class ProfileController:
    def __init__(self, menu_controller):
        self.menu_controller = menu_controller

    @staticmethod
    async def profile(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        keyboard = [
            [
                InlineKeyboardButton(
                    "Редактировать", callback_data="profile:edit_profile"
                )
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        tg_id = update.message.from_user.id
        try:
            await update.message.reply_text(
                (await ProfileService.get_profile_info(tg_id)),
                reply_markup=reply_markup,
                parse_mode="Markdown",
            )
        except UserNotExistsException:
            await update.message.reply_text("Вы не зарегистрированы")

        return ConversationStates.MENU

    async def handle_edit_profile_inline_buttons(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        query = update.callback_query
        await query.answer()

        match query.data:
            case "profile:edit_profile":
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "Редактировать имя", callback_data="profile:edit_name"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Редактировать страну", callback_data="profile:edit_country"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "Редактировать город", callback_data="profile:edit_city"
                        )
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_reply_markup(reply_markup=reply_markup)
            case "profile:edit_name":
                await query.message.reply_text("Введите новое имя:")
                return ConversationStates.EDIT_PROFILE_NAME
            case "profile:edit_city":
                await query.message.reply_text("Введите новый город:")
                return ConversationStates.EDIT_PROFILE_CITY
            case "profile:edit_country":
                await query.message.reply_text("Введите новую страну:")
                return ConversationStates.EDIT_PROFILE_COUNTRY

        return ConversationStates.MENU

    async def edit_profile_name(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        tg_id = update.message.from_user.id
        text = update.message.text

        await ProfileService.set_user_name(tg_id, text)
        answer = "Имя успешно изменено."

        await self.menu_controller.show_main_menu(update, context, message=answer)
        await ProfileController.profile(update, context)

        return ConversationStates.MENU

    async def edit_profile_city(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        tg_id = update.message.from_user.id
        text = update.message.text

        await ProfileService.set_user_city(tg_id, text)
        answer = "Город успешно изменен."

        await self.menu_controller.show_main_menu(update, context, message=answer)
        await ProfileController.profile(update, context)

        return ConversationStates.MENU

    async def edit_profile_country(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        tg_id = update.message.from_user.id
        text = update.message.text

        await ProfileService.set_user_country(tg_id, text)
        answer = "Страна успешно изменена."

        await self.menu_controller.show_main_menu(update, context, message=answer)
        await ProfileController.profile(update, context)

        return ConversationStates.MENU
