from sqlalchemy import Column, Integer, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class UserGenre(Base):
    __tablename__ = 'UserGenres'
    
    id_ = Column(Integer, Sequence('user_genre_id_seq'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)
    genre_id = Column(Integer, ForeignKey('Genres.id_'), nullable=False)

    user = relationship('User', back_populates='user_genres')
    genre = relationship('Genre', back_populates='user_genres')

    def __repr__(self):
        return f"UserGenre(user_id={self.user_id}, genre_id='{self.genre_id}'"
