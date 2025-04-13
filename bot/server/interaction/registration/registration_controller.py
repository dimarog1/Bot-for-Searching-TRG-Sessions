from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.enums.country_codes import CountryCodes
from bot.server.interaction.conversation_states import ConversationStates
from bot.server.interaction.menu import MenuController
from bot.server.interaction.registration.registration_service import RegistrationService
from bot.utils import geo_utils


class RegistrationController:
    def __init__(self, menu_controller):
        self.menu_controller = menu_controller

    async def register_user(self, tg_id: int, user_data: dict) -> None:
        try:
            await RegistrationService.register_user(
                tg_id,
                user_data.get("name", ""),
                user_data.get("country", ""),
                user_data.get("city", ""),
            )
        except Exception as e:
            print(f"Ошибка при регистрации пользователя: {e}")

    async def start_register(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        tg_id = update.message.from_user.id

        if await RegistrationService.is_registered(tg_id):
            await MenuController.show_main_menu(update, context)
            return ConversationStates.MENU

        if "registration_data" not in context.user_data:
            context.user_data["registration_data"] = {}

        context.user_data["registration_data"]["tg_id"] = tg_id

        await update.message.reply_text(
            "О, похоже, что Вы впервые тут! Давайте знакомиться)"
        )
        await update.message.reply_text("Укажите Ваше имя:")
        return ConversationStates.ENTER_PROFILE_NAME

    async def input_name(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        context.user_data["registration_data"]["name"] = update.message.text

        keyboard = [
            [
                InlineKeyboardButton(country.value, callback_data=country.value)
                for country in CountryCodes
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Выберите страну из списка:", reply_markup=reply_markup
        )

        return ConversationStates.ENTER_PROFILE_COUNTRY

    async def input_country(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        context.user_data["registration_data"]["country"] = update.callback_query.data

        await update.callback_query.message.reply_text("Укажите Ваш город:")
        return ConversationStates.ENTER_PROFILE_CITY

    async def input_city(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        tg_id = update.message.from_user.id
        city = update.message.text
        country = context.user_data["registration_data"]["country"]

        value_to_key = {
            country_code.value: country_code.name for country_code in CountryCodes
        }
        if not geo_utils.get_location(value_to_key[country], city):
            await update.message.reply_text(
                "Такого города не существует. Попробуйте еще раз."
            )
            return await self.input_country(update, context)

        context.user_data["registration_data"]["city"] = city.capitalize()

        await self.register_user(tg_id, context.user_data["registration_data"])
        await update.message.reply_text("Вы успешно зарегистрированы!")

        await self.menu_controller.show_main_menu(update, context)

        if "registration_data" in context.user_data:
            del context.user_data["registration_data"]

        return ConversationStates.MENU

    async def cancel(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> ConversationStates:
        if "registration_data" in context.user_data:
            del context.user_data["registration_data"]

        await update.message.reply_text("Регистрация отменена.")
        return ConversationStates.MENU
