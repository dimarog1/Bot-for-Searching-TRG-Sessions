from sqlalchemy import Column, Integer, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from bot.db import DeclarativeBase


class Recommendation(DeclarativeBase):
    __tablename__ = 'Recommendations'

    id_ = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)
    game_id = Column(Integer, ForeignKey('Games.id_'), nullable=False)
    session_id = Column(Integer, ForeignKey('Sessions.id_'), nullable=False)

    user = relationship('User', back_populates='recommendations')
    game = relationship('Game', back_populates='recommendations')
    session = relationship('Session', back_populates='recommendations')

    def __repr__(self):
        return f"Recommendation(id_={self.user_id}, user_id='{self.genre_id}'"
