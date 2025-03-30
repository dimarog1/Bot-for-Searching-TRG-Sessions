from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ARRAY, ForeignKey, func
from sqlalchemy.orm import relationship

from bot.db import DeclarativeBase


class Session(DeclarativeBase):
    __tablename__ = 'Sessions'

    id_ = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    genre_ids = Column(ARRAY(Integer))
    game_name = Column(String(50), nullable=False)
    master_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)
    country = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    is_online = Column(Boolean, default=False)
    max_players = Column(Integer, nullable=False)
    current_players = Column(Integer, nullable=False)
    start_datetime = Column(DateTime, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    reviews = relationship('Review', back_populates='session')
    session_players = relationship('SessionPlayer', back_populates='session')
    recommendations = relationship('Recommendation', back_populates='session')

    master = relationship('User', back_populates='sessions')

    def __repr__(self):
        return f"Session(id={self.id_}, game_id={self.game_id}, master_id={self.master_id})"
