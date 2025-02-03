from sqlalchemy import Column, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from bot.db import DeclarativeBase


class SessionPlayer(DeclarativeBase):
    __tablename__ = 'SessionPlayers'

    id_ = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    session_id = Column(Integer, ForeignKey('Sessions.id_'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)

    user = relationship('User', back_populates='session_players')
    session = relationship('Session', back_populates='session_players')

    def __repr__(self):
        return f"Session(id_={self.id_}, game_id='{self.game_id}' , master_id='{self.master_id}'"
