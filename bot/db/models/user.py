from sqlalchemy import Column, Integer, String, Boolean, Float, TIMESTAMP, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id_ = Column(Integer, Sequence('user_id_seq'), primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    tg_id = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False)
    country = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    rating = Column(Float, default=0.0)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)

    logs = relationship('Log', back_populates='user')
    reviews = relationship('Review', back_populates='user')
    sessions = relationship('Session', back_populates='master')
    session_players = relationship('SessionPlayer', back_populates='user')
    recomendations = relationship('Recomendation', back_populates='user')
    user_genres = relationship('UserGenre', back_populates='user')

    def __repr__(self):
        return f"User(id={self.id_}, name='{self.name}'"
