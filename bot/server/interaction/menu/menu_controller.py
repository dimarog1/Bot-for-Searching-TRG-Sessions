import enum

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.db.models import User
from bot.server.common_dao import UserDao


class MenuStatesEnum(enum.Enum):
    MENU = "Меню"
    PROFILE = "Профиль"
    SESSIONS = "Сессии"
    MASTER_SEARCH = "Поиск мастеров"
    SETTINGS = "Настройки"
    SUPPORT = "Помощь"


class MenuController:
    async def show_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [
                MenuStatesEnum.PROFILE.value,
                MenuStatesEnum.SESSIONS.value,
                MenuStatesEnum.MASTER_SEARCH.value,
                MenuStatesEnum.SETTINGS.value
            ],
            [
                MenuStatesEnum.SUPPORT.value
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

        await update.message.reply_text("Вам доступно меню", reply_markup=reply_markup)

    async def main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text

        match text:
            case MenuStatesEnum.PROFILE.value:
                await self.profile(update, context)
            case MenuStatesEnum.SESSIONS.value:
                raise NotImplementedError(f"{MenuStatesEnum.SESSIONS.value} not implemented yet")
            case MenuStatesEnum.MASTER_SEARCH.value:
                raise NotImplementedError(f"{MenuStatesEnum.MASTER_SEARCH.value} not implemented yet")
            case MenuStatesEnum.SETTINGS.value:
                raise NotImplementedError(f"{MenuStatesEnum.SETTINGS.value} not implemented yet")
            case MenuStatesEnum.SUPPORT.value:
                await self.support(update, context)

    async def profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("Редактировать", callback_data="edit_data")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        tg_id = update.message.from_user.id
        user = await UserDao.get_user_by_tg_id(tg_id)

        if user is not None:
            profile_info = (f"Имя: {user.name}\n"
                            f"Страна: {user.country}\n"
                            f"Город: {user.city}\n"
                            f"Рейтинг: {user.rating}")
            await update.message.reply_text(profile_info, reply_markup=reply_markup)
        else:
            await update.message.reply_text("Вы не зарегистрированы, чтобы зарегистрироваться напишите /register")

    async def support(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Напишите нам: @support_bot")

    async def handle_inline_buttons(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        
        match query.data:
            case "edit_data":
                await query.edit_message_text("Редактирование данных: ...")
