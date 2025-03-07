from sqlalchemy import text

from bot.db.models import User

from bot.db.connection import SessionManager


class UserDao:

    @staticmethod
    async def write_user_to_db(user: User) -> User:
        async with SessionManager.get_session() as session:
            session.add(user)
            await session.commit()

        return user

    @staticmethod
    async def get_user_by_tg_id(tg_id: int) -> User | None:
        query = text("""SELECT * 
                        FROM "Users"
                        WHERE tg_id = :tg_id""")

        async with SessionManager.get_session() as session:
            user = (await session.execute(query, {"tg_id": tg_id})).first()

        return user
