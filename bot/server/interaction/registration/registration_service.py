from bot.db.models import User
from bot.server.common_dao.user_dao import UserDao


class RegistrationService:
    @staticmethod
    async def is_registered(tg_id: int) -> bool:
        return await UserDao.get_user_by_tg_id(tg_id) is not None

    @staticmethod
    async def register_user(
            tg_id: int,
            tg_username: str,
            name: str,
            country: str,
            city: str,
    ) -> User:
        user = User(tg_id=tg_id, tg_username = tg_username, name=name, country=country, city=city)

        return await UserDao.write_user_to_db(user)
