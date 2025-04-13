from sqlalchemy import exists, select, text

from bot.db.connection import SessionManager
from bot.db.models import Session


class SessionDao:

    @staticmethod
    async def write_session_to_db(game_session: Session) -> Session:
        async with SessionManager.get_session() as session:
            session.add(game_session)
            await session.commit()

        return game_session

    @staticmethod
    async def get_all_sessions() -> list[Session]:
        query = select(Session)

        async with SessionManager.get_session() as session:
            result = (await session.execute(query)).scalars().all()

        return result

    @staticmethod
    async def get_sessions_by_game_name(game_name: str) -> Session:
        query = text(
            """SELECT s.*
                        FROM "Sessions" s
                        JOIN "Games" g ON s.game_id = g.id_
                        WHERE g.name LIKE ':game_name'"""
        )

        async with SessionManager.get_session() as session:
            result = (await session.execute(query, {"game_name": game_name})).scalar()

        return result

    @staticmethod
    async def get_sessions_by_master(master: str) -> Session:
        query = text(
            """SELECT s.*
                        FROM "Sessions" s
                        JOIN "Users" u ON s.master_id = u.id_
                        WHERE u.name LIKE 'master'"""
        )

        async with SessionManager.get_session() as session:
            result = (await session.execute(query, {"master": master})).scalar()

        return result

    @staticmethod
    async def get_sessions_by_max_players(max_players: int, comparator: str) -> Session:
        query = text(
            """SELECT s.*
                        FROM "Sessions" s
                        WHERE s.max_players :comparator :max_players"""
        )

        async with SessionManager.get_session() as session:
            result = (
                await session.execute(
                    query, {"max_players": max_players, "comparator": comparator}
                )
            ).scalar()

        return result

    @staticmethod
    async def get_sessions_by_location(country: str, city: str) -> Session:
        query = text(
            """SELECT *
                        FROM "Sessions"
                        WHERE country = :country AND city = :city"""
        )

        async with SessionManager.get_session() as session:
            result = (
                await session.execute(query, {"country": country, "city": city})
            ).scalar()

        return result
