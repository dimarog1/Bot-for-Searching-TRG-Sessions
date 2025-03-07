from dataclasses import dataclass
import enum
import traceback

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.utils import geo_utils
from bot.enums.country_codes import CountryCodes

from bot.server.interaction.registration.registration_service import RegistrationService


@dataclass
class InputUserData:
    tg_id: int = 0
    name: str = ""
    country: str = ""
    city: str = ""


class StatesEnum(enum.Enum):
    NAME = 0
    COUNTRY = 1
    CITY = 2


class RegistrationController:

    def __init__(self):
        self.users_data: dict[int, InputUserData] = dict()

    async def register_user(self, tg_id: int) -> None:
        try:
            user = self.users_data[tg_id]
            await RegistrationService.register_user(user.tg_id, user.name, user.country, user.city)
        except Exception:
            print(traceback.format_exc())

    async def start_register(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        
        if await RegistrationService.is_registered(tg_id):
            await update.message.reply_text("Вы уже зарегистрированы.")
            return ConversationHandler.END

        self.users_data[tg_id] = InputUserData(tg_id=tg_id)
        
        await update.message.reply_text("Укажите Ваше имя:")
        return StatesEnum.NAME

    async def input_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.users_data[tg_id].name = update.message.text

        keyboard = [
            [InlineKeyboardButton(country.value, callback_data=country.value) for country in CountryCodes]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Выберите страну из списка:", reply_markup=reply_markup)

        return StatesEnum.COUNTRY

    async def input_country(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.callback_query.from_user.id
        self.users_data[tg_id].country = update.callback_query.data

        await update.callback_query.message.reply_text("Укажите Ваш город:")
        return StatesEnum.CITY

    async def input_city(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id

        value_to_key = {country_code.value: country_code.name for country_code in CountryCodes}
        if not geo_utils.get_location(value_to_key[self.users_data[tg_id].country], update.message.text):
            await update.message.reply_text("Такого города не существует. Попробуйте еще раз.")
            return await self.input_country(update, context)

        self.users_data[tg_id].city = update.message.text.capitalize()

        await self.register_user(tg_id)

        await update.message.reply_text("Вы успешно зарегистрированы!")

        self.clear_user_data(tg_id)
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.clear_user_data(tg_id)

        await update.message.reply_text('Регистрация отменена.')

        return ConversationHandler.END

    def clear_user_data(self, tg_id: int) -> None:
        del self.users_data[tg_id]
