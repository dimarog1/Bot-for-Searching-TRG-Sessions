import enum

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.exceptions.registration_exceptions import UserNotExistsException
from bot.server.interaction.menu.menu_service import MenuService


class MenuStatesEnum(enum.Enum):
    MENU = "Меню"
    PROFILE = "Профиль"
    SESSIONS = "Сессии"
    MASTER_SEARCH = "Поиск мастеров"
    SETTINGS = "Настройки"
    SUPPORT = "Помощь"
    EDIT_NAME = "Редактировать имя"
    EDIT_CITY = "Редактировать город"
    EDIT_COUNTRY = "Редактировать страну"


class MenuController:
    @staticmethod
    async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message="Вам доступно меню"):
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

        await update.message.reply_text(message, reply_markup=reply_markup)

    @staticmethod
    async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = update.message.text

        match text:
            case MenuStatesEnum.PROFILE.value:
                await MenuController.profile(update, context)
            case MenuStatesEnum.SESSIONS.value:
                raise NotImplementedError(f"{MenuStatesEnum.SESSIONS.value} is not implemented yet")
            case MenuStatesEnum.MASTER_SEARCH.value:
                raise NotImplementedError(f"{MenuStatesEnum.MASTER_SEARCH.value} is not implemented yet")
            case MenuStatesEnum.SETTINGS.value:
                raise NotImplementedError(f"{MenuStatesEnum.SETTINGS.value} is not implemented yet")
            case MenuStatesEnum.SUPPORT.value:
                await MenuController.support(update, context)

    @staticmethod
    async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("Редактировать", callback_data="edit_profile")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        tg_id = update.message.from_user.id
        try:
            await update.message.reply_text(
                (await MenuService.get_profile_info(tg_id)),
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
        except UserNotExistsException:
            await update.message.reply_text("Вы не зарегистрированы.\nПожалуйста, воспользуйтесь командой /register")

    @staticmethod
    async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("По всем вопросам по боту обращайтесь к Дмитрию (@dimarog1) или Антону (@mureann)")

    @staticmethod
    async def handle_inline_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        match query.data:
            case "edit_profile":
                keyboard = [
                    [InlineKeyboardButton("Редактировать имя", callback_data="edit_name")],
                    [InlineKeyboardButton("Редактировать страну", callback_data="edit_country")],
                    [InlineKeyboardButton("Редактировать город", callback_data="edit_city")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_reply_markup(reply_markup=reply_markup)
            case "edit_name":
                await query.message.reply_text("Введите новое имя:")
                context.user_data['state'] = MenuStatesEnum.EDIT_NAME
            case "edit_city":
                await query.message.reply_text("Введите новый город:")
                context.user_data['state'] = MenuStatesEnum.EDIT_CITY
            case "edit_country":
                await query.message.reply_text("Введите новую страну:")
                context.user_data['state'] = MenuStatesEnum.EDIT_COUNTRY

    @staticmethod
    async def handle_user_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        state = context.user_data.get('state')
        tg_id = update.message.from_user.id
        text = update.message.text

        answer = "Что-то пошло не так, попробуйте еще раз."

        if state == MenuStatesEnum.EDIT_NAME:
            await MenuService.set_user_name(tg_id, text)
            answer = "Имя успешно изменено."
        elif state == MenuStatesEnum.EDIT_CITY:
            await MenuService.set_user_city(tg_id, text)
            answer = "Город успешно изменен."
        elif state == MenuStatesEnum.EDIT_COUNTRY:
            await MenuService.set_user_country(tg_id, text)
            answer = "Страна успешно изменена."

        context.user_data['state'] = None

        await MenuController.show_menu(update, context, message=answer)
        await MenuController.profile(update, context)
