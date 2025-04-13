from functools import wraps

from bot.exceptions.registration_exceptions import UserNotExistsException
from bot.server.common_dao import UserDao


def registration_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tg_id = kwargs.get("tg_id") or (args[0] if args else None)
        if tg_id is None:
            raise ValueError("tg_id is required")

        if not (await UserDao.get_user_by_tg_id(tg_id)):
            raise UserNotExistsException("Пользователь не зарегистрирован")

        return await func(*args, **kwargs)

    return wrapper
