from dataclasses import dataclass
import datetime
import enum
import traceback

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.server.interaction.sessions.session_service import SessionService
from bot.server.common_dao.user_dao import UserDao


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
    START_DATETIME = 5
    DURATION_HOURS = 6


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
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id].max_players = int(update.message.text)
        
        await update.message.reply_text("Когда начнем игру? (формат: YYYY-MM-DD HH:MM):")
        return StatesEnum.START_DATETIME

    async def input_start_datetime(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id].start_datetime = datetime.datetime.strptime(update.message.text, "%Y-%m-%d %H:%M")
        
        await update.message.reply_text("Сколько она будет приблизительно идти?")
        return StatesEnum.DURATION_HOURS

    async def input_duration_hours(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tg_id = update.message.from_user.id
        self.sessions_data[tg_id].duration_hours = int(update.message.text)
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