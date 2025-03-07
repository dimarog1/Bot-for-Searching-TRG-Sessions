from bot.db.models import User

from bot.exceptions.registration_exceptions import UserAlreadyExistsException

from bot.server.common_dao import UserDao


class RegistrationService:

    @staticmethod
    async def is_registered(tg_id: int) -> bool:
        return await UserDao.get_user_by_tg_id(tg_id) is not None

    @staticmethod
    async def register_user(
            tg_id: int,
            name: str,
            country: str,
            city: str,
    ) -> User:
        if await RegistrationService.is_registered(tg_id):
            raise UserAlreadyExistsException("Пользователь уже зарегистрирован")

        user = User(tg_id=tg_id, name=name, country=country, city=city)

        return await UserDao.write_user_to_db(user)
