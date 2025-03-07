from bot.server.common_dao.user_dao import UserDao
from bot.server.interaction.registration.registration_service import RegistrationService


class StartChatService:

    @staticmethod
    async def get_meeting_message(tg_id: int) -> str:
        registered = await RegistrationService.is_registered(tg_id)

        if registered:
            user = await UserDao.get_user_by_tg_id(tg_id)
            return f"Привет, {user.name}! Чтобы посмотреть информацию о профиле используйте команду /profile"

        return "Привет! Я бот для поиска TRG сессий. Чтобы зарегистрироваться, используйте команду /register"
