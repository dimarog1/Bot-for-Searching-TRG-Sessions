from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from bot.db import DeclarativeBase


class Game(DeclarativeBase):
    __tablename__ = 'Games'

    id_ = Column(Integer, ForeignKey('Games.id_'), autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    genre_id = Column(Integer, ForeignKey('Genres.id_'), nullable=False)

    sessions = relationship('Session', back_populates='game')
    recommendations = relationship('Recommendation', back_populates='game')

    genre = relationship('Genre', back_populates='games')

    def __repr__(self):
        return f"Game(id={self.id_}, name={self.name}, genre_id={self.genre_id})"
