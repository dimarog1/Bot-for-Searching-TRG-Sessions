from sqlalchemy import Column, Integer, String, DateTime, Sequence, ForeignKey, func
from sqlalchemy.orm import relationship

from bot.db import DeclarativeBase


class Log(DeclarativeBase):
    __tablename__ = 'Logs'

    id_ = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)
    action = Column(String(50), nullable=False)
    details = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship('User', back_populates='logs')

    def __repr__(self):
        return f"Genre(id={self.id_}, name='{self.name}'"
