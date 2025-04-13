from sqlalchemy import exists, select, text

from bot.db.connection import SessionManager
from bot.db.models import User


class UserDao:

    @staticmethod
    async def write_user_to_db(user: User) -> User:
        async with SessionManager.get_session() as session:
            session.add(user)
            await session.commit()

        return user

    @staticmethod
    async def get_user_by_id(id_: int) -> User | None:
        query = text("""SELECT * 
                        FROM "Users"
                        WHERE id_ = :id_""")

        async with SessionManager.get_session() as session:
            user = (await session.execute(query, {"id_": id_})).first()

        return user

    @staticmethod
    async def get_user_by_tg_id(tg_id: int) -> User | None:
        query = text(
            """SELECT * 
                        FROM "Users"
                        WHERE tg_id = :tg_id"""
        )

        async with SessionManager.get_session() as session:
            user = (await session.execute(query, {"tg_id": tg_id})).first()

        return user

    @staticmethod
    async def set_user_name(tg_id: int, new_name: str) -> User | None:
        query = text(
            """UPDATE "Users" 
                        SET name = :name 
                        WHERE tg_id = :tg_id 
                        RETURNING *"""
        )

        async with SessionManager.get_session() as session:
            user = (
                await session.execute(query, {"tg_id": tg_id, "name": new_name})
            ).first()
            await session.commit()

        return user

    @staticmethod
    async def set_user_city(tg_id: int, new_city: str) -> User | None:
        query = text(
            """UPDATE "Users" 
                        SET city = :city 
                        WHERE tg_id = :tg_id 
                        RETURNING *"""
        )

        async with SessionManager.get_session() as session:
            user = (
                await session.execute(query, {"tg_id": tg_id, "city": new_city})
            ).first()
            await session.commit()

        return user

    @staticmethod
    async def set_user_country(tg_id: int, new_country: str) -> User | None:
        query = text(
            """UPDATE "Users" 
                        SET country = :country 
                        WHERE tg_id = :tg_id 
                        RETURNING *"""
        )

        async with SessionManager.get_session() as session:
            user = (
                await session.execute(query, {"tg_id": tg_id, "country": new_country})
            ).first()
            await session.commit()

        return user

    @staticmethod
    async def set_user_rating(tg_id: int, new_rating: str) -> User | None:
        query = text(
            """UPDATE "Users" 
                        SET rating = :new_rating 
                        WHERE tg_id = :tg_id 
                        RETURNING *"""
        )

        async with SessionManager.get_session() as session:
            user = (
                await session.execute(query, {"tg_id": tg_id, "rating": new_rating})
            ).first()
            await session.commit()

        return user
