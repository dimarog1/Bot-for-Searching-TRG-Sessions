import textwrap

from bot.db.models import User
from bot.server.common_dao import UserDao
from bot.utils.registration_utils import registration_required


class MenuService:

    @staticmethod
    @registration_required
    async def get_profile_info(tg_id: int) -> str:
        user = await UserDao.get_user_by_tg_id(tg_id)

        user_profile_info = textwrap.dedent(f"""
            👤*Имя*: {user.name}
            📍*Локация*: {user.country}, {user.city}
            ⭐️*Рейтинг*: {user.rating}
            """).strip()

        return user_profile_info

    @staticmethod
    @registration_required
    async def set_user_name(tg_id: int, new_name: str) -> User:
        return await UserDao.set_user_name(tg_id, new_name)

    @staticmethod
    @registration_required
    async def set_user_city(tg_id: int, new_city: str) -> User:
        return await UserDao.set_user_city(tg_id, new_city)

    @staticmethod
    @registration_required
    async def set_user_country(tg_id: int, new_country: str) -> User:
        return await UserDao.set_user_country(tg_id, new_country)

