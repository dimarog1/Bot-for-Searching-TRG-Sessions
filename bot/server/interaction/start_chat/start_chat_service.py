from bot.server.common_dao import UserDao
from bot.server.interaction.registration.registration_service import RegistrationService


class StartChatService:

    @staticmethod
    async def get_meeting_message(tg_id: int) -> str:
        registered = await RegistrationService.is_registered(tg_id)

        if registered:
            user = await UserDao.get_user_by_tg_id(tg_id)
            return f"Привет, {user.name}!\nОсновное меню находится ниже - у вас в клавиатуре.\n" \

        return "О, похоже, что Вы впервые тут!\nЧтобы зарегистрироваться, воспользуйтесь /register"