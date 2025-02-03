from sqlalchemy import Column, Integer, String, DateTime, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Log(Base):
    __tablename__ = 'Logs'

    id_ = Column(Integer, Sequence('log_id_seq'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)
    action = Column(String(50), nullable=False)
    details = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='logs')

    def __repr__(self):
        return f"Genre(id={self.id_}, name='{self.name}'"
