from sqlalchemy import Boolean, Column, DateTime, Float, Integer, Sequence, String, func
from sqlalchemy.orm import relationship

from bot.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = "Users"

    id_ = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    tg_id = Column(Integer, nullable=False)
    tg_username = Column(String(50), nullable=True)
    is_admin = Column(Boolean, default=False)
    country = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    logs = relationship("Log", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    sessions = relationship("Session", back_populates="master")
    session_players = relationship("SessionPlayer", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")
    user_genres = relationship("UserGenre", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id_}, tg_username='{self.tg_username}')"
