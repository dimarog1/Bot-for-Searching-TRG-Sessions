from bot.db.models import Session
from bot.server.interaction.sessions.session_dao import SessionDao


class SessionService:

    @staticmethod
    async def create_session(
        user_id: int,
        game_name: str,
        country: str,
        city: str,
        is_online: bool,
        max_players: int,
        start_datetime: str,
        duration_hours: int,
    ) -> Session:
        session = Session(
            master_id=user_id,
            game_name=game_name,
            country=country,
            city=city,
            is_online=is_online,
            max_players=max_players,
            current_players=0,
            start_datetime=start_datetime,
            duration_hours=duration_hours,
        )

        return await SessionDao.write_session_to_db(session)

    @staticmethod
    async def get_all_sessions() -> list[Session]:
        return await SessionDao.get_all_sessions()