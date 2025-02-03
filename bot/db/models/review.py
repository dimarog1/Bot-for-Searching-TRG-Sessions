from sqlalchemy import Column, Integer, String, Float, DateTime, Sequence, ForeignKey, func
from sqlalchemy.orm import relationship

from bot.db import DeclarativeBase


class Review(DeclarativeBase):
    __tablename__ = 'Reviews'

    id_ = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    session_id = Column(Integer, ForeignKey('Sessions.id_'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)
    rating = Column(Float, default=0.0)
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    user = relationship('User', back_populates='reviews')
    session = relationship('Session', back_populates='reviews')

    def __repr__(self):
        return f"User(id={self.id_}, name='{self.name}'"
