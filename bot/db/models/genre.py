from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship

from bot.db import DeclarativeBase


class Genre(DeclarativeBase):
    __tablename__ = 'Genres'

    id_ = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)

    user_genres = relationship('UserGenre', back_populates='genre')
    games = relationship('Game', back_populates='genre')

    def __repr__(self):
        return f"Genre(id={self.id_}, name='{self.name}'"
