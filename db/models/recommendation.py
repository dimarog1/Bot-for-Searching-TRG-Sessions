from sqlalchemy import Column, Integer, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Recommendation(Base):
    __tablename__ = 'Recommendations'

    id_ = Column(Integer, Sequence('recommendation_id_seq'), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)
    game_id = Column(Integer, ForeignKey('Games.id_'), nullable=False)
    session_id = Column(Integer, ForeignKey('Sessions.id_'), nullable=False)

    def __repr__(self):
        return f"Recommendation(id_={self.user_id}, user_id='{self.genre_id}'"
