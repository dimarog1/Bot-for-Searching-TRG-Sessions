from dataclasses import dataclass
import datetime
import enum
import traceback

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram_bot_calendar import DetailedTelegramCalendar

from bot.server.interaction.sessions.session_service import SessionService
from bot.server.common_dao.user_dao import UserDao


STEP_RU = {'y': 'год', 'm': 'месяц', 'd': 'день'}

@dataclass
class InputSessionData:
    tg_id: int = 0
    master_id: int = -1
    game_name: str = ""
    country: str = ""
    city: str = ""
    is_online: bool = False
    max_players: int = 0
    start_datetime: datetime.datetime = ""
    duration_hours: int = 0


class StatesEnum(enum.Enum):
    GAME_NAME = 0
    COUNTRY = 1
    CITY = 2
    IS_ONLINE = 3
    MAX_PLAYERS = 4
    START_DATE = 5
    START_TIME = 6
    DURATION_HOURS = 7


class BriefCalendar(DetailedTelegramCalendar):
    locale = 'ru'
    prev_button = '⬅️'
    next_button = '➡️'
    empty_nav_button = ''
    middle_button_year = ''
    empty_month_button = ''
    empty_year_button = ''
    days_of_week = {'ru': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']}

class SessionController:

    def __init__(self):
        self.sessions_data: dict[int, InputSessionData] = dict()

    async def create_session(self, tg_id: int) -> None:
        try:
            session = self.sessions_data[tg_id]
            await SessionService.create_session(session.master_id, session.game_name, session.country, session.city, session.is_online, session.max_players, session.start_datetime, session.duration_hours)
        except Exception:
            print(traceback.format_exc())

    async def start_session_creation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id] = InputSessionData(tg_id=tg_id)
        self.sessions_data[tg_id].master_id = (await UserDao.get_user_by_tg_id(tg_id)).id_
        await update.message.reply_text("Во что будем играть?")
        return StatesEnum.GAME_NAME

    async def input_game_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id].game_name = update.message.text
        keyboard = [
            [InlineKeyboardButton("Да", callback_data='yes'), InlineKeyboardButton("Нет", callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Планируете провести игру онлайн?",
            reply_markup=reply_markup
        )
        return StatesEnum.IS_ONLINE

    async def input_is_online(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        tg_id = query.from_user.id
        is_online = query.data == 'yes'
        self.sessions_data[tg_id].is_online = is_online

        await query.answer()

        if is_online:
            self.sessions_data[tg_id].country = "online"
            self.sessions_data[tg_id].city = "online"
            await query.edit_message_text("Сколько игроков планируется?")
            return StatesEnum.MAX_PLAYERS
        else:
            await query.edit_message_text("В какой стране играем?")
            return StatesEnum.COUNTRY

    async def input_country(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id].country = update.message.text
        
        await update.message.reply_text("А теперь укажите город:")
        return StatesEnum.CITY

    async def input_city(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id].city = update.message.text
        
        await update.message.reply_text("Сколько игроков планируется?")
        return StatesEnum.MAX_PLAYERS

    async def input_max_players(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            max_players = int(update.message.text)
            if max_players <= 1 or max_players > 20:
                raise ValueError
        except ValueError:
            await update.message.reply_text("Пожалуйста, укажите корректное количество игроков (от 2 до 20):")
            return StatesEnum.MAX_PLAYERS
        
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id].max_players = max_players

        calendar, step = BriefCalendar(
            min_date=datetime.date.today(),
            max_date=datetime.date.today() + datetime.timedelta(days=30),
            locale='ru'
        ).build()
        await update.message.reply_text(f"Выберите дату ({STEP_RU[step]}):", reply_markup=calendar)
        return StatesEnum.START_DATE

    async def input_start_date(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        tg_id = query.from_user.id

        result, key, step = BriefCalendar(
            min_date=datetime.date.today(),
            max_date=datetime.date.today() + datetime.timedelta(days=30),
            locale='ru'
        ).process(query.data)
        
        if not result and key:
            await query.edit_message_text(f"*Дата проведения ({STEP_RU[step]})*", reply_markup=key, parse_mode='Markdown')
            return StatesEnum.START_DATE

        self.sessions_data[tg_id].start_datetime = result

        await query.edit_message_text(f"Сессия состоится в этот день: *{result.strftime('%d.%m.%Y')}*", parse_mode='Markdown')
        await query.message.reply_text("Во сколько начнем?", reply_markup=self.get_time_keyboard())
        return StatesEnum.START_TIME

    def get_time_keyboard(self):
        buttons = []
        for hour in range(8, 21):
            buttons.append([
                InlineKeyboardButton(f"{hour:02d}:00", callback_data=f"{hour:02d}:00"),
                InlineKeyboardButton(f"{hour:02d}:30", callback_data=f"{hour:02d}:30")
            ])
        return InlineKeyboardMarkup(buttons)

    async def input_start_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        tg_id = query.from_user.id
        time_str = query.data

        self.sessions_data[tg_id].start_datetime = datetime.datetime.combine(self.sessions_data[tg_id].start_datetime, datetime.datetime.strptime(time_str, "%H:%M").time())
        
        await query.edit_message_text(f"Игра начнется в *{time_str}* по местному времени.", parse_mode='Markdown')
        await query.message.reply_text(f"На сколько часов она планируется?")

        return StatesEnum.DURATION_HOURS

    async def input_duration_hours(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        try:
            duration_hours = int(update.message.text)
            if duration_hours <= 0 or duration_hours > 10:
                raise ValueError
        except ValueError:
            await update.message.reply_text("Пожалуйста, укажите корректную продолжительность сессии (от 1 до 10 часов):")
            return StatesEnum.DURATION_HOURS
        
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id].duration_hours = duration_hours
        await self.create_session(tg_id)
        await update.message.reply_text("Сессия успешно создана!")
        
        self.clear_session_data(tg_id)
        return ConversationHandler.END
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.clear_session_data(tg_id)

        await update.message.reply_text('Создание сессии отменено.')
        return ConversationHandler.END

    def clear_session_data(self, tg_id: int) -> None:
        del self.sessions_data[tg_id]