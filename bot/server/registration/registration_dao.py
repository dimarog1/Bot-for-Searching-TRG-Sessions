from sqlalchemy import exists, select

from bot.db.models import User

from bot.db.connection import SessionManager


class RegistrationDao:

    @staticmethod
    async def write_user_to_db(user: User) -> User:
        async with SessionManager.get_session() as session:
            session.add(user)
            await session.commit()

        return user

    @staticmethod
    async def get_user_by_tg_id(tg_id: int):
        query = select(exists().where(User.tg_id == tg_id))

        async with SessionManager.get_session() as session:
            result = (await session.execute(query)).scalar()

        return result
