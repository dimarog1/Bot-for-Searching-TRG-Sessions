from dataclasses import dataclass
import enum
import traceback

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .registration_service import RegistrationService


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
        self.users_data[tg_id] = InputUserData(tg_id=tg_id)
        
        await update.message.reply_text("Пожалуйста, введите Ваше имя:")
        
        return StatesEnum.NAME.value

    async def input_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.users_data[tg_id].name = update.message.text
        
        await update.message.reply_text("Теперь введите Вашу страну:")
        
        return StatesEnum.COUNTRY.value

    async def input_country(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.users_data[tg_id].country = update.message.text

        await update.message.reply_text("Теперь введите Ваш город:")

        return StatesEnum.CITY.value

    async def input_city(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.users_data[tg_id].city = update.message.text

        await self.register_user(tg_id)

        await update.message.reply_text("Теперь Вы зарегистрированы!")

        self.clear_user_data(tg_id)

        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.clear_user_data(tg_id)

        await update.message.reply_text('Регистрация отменена.')

        return ConversationHandler.END

    def clear_user_data(self, tg_id: int) -> None:
        del self.users_data[tg_id]
