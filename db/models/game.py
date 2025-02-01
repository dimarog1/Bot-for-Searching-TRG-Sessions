from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Game(Base):
    __tablename__ = 'Games'

    id_ = Column(Integer, Sequence('game_id_seq'), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    genre_id = Column(Integer, ForeignKey('Genres.id_'), nullable=False)

    def __repr__(self):
        return f"Game(user_id={self.id_}, genre_id='{self.name}'"
