from bot.db.models import User

from bot.exceptions.registration_exceptions import UserAlreadyExistsException

from .registration_dao import RegistrationDao


class RegistrationService:

    @staticmethod
    async def is_registered(tg_id: int) -> bool:
        return await RegistrationDao.get_user_by_tg_id(tg_id)

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

        return await RegistrationDao.write_user_to_db(user)
