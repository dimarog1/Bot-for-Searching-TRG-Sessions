from sqlalchemy import select

from bot.db.connection import SessionManager
from bot.db.models import User


class StartChatDao:

    @staticmethod
    async def get_user(tg_id: int) -> User:
        query = select(User).where(User.tg_id == tg_id)

        async with SessionManager.get_session() as session:
            result = (await session.execute(query)).scalar()

        return result
