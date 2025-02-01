from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Genre(Base):
    __tablename__ = 'Genres'

    id_ = Column(Integer, Sequence('genre_id_seq'), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"Genre(id={self.id_}, name='{self.name}'"
