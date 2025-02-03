from sqlalchemy import Column, Integer, String, Float, DateTime, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Review(Base):
    __tablename__ = 'Reviews'

    id_ = Column(Integer, Sequence('review_id_seq'), primary_key=True, nullable=False)
    session_id = Column(Integer, ForeignKey('Sessions.id_'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)
    rating = Column(Float, default=0.0)
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    user = relationship('User', back_populates='reviews')
    session = relationship('Session', back_populates='reviews')

    def __repr__(self):
        return f"User(id={self.id_}, name='{self.name}'"
