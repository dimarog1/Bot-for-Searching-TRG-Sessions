from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SessionPlayer(Base):
    __tablename__ = 'SessionPlayers'

    id_ = Column(Integer, Sequence('session_player_id_seq'), primary_key=True, nullable=False)
    session_id = Column(Integer, ForeignKey('Sessions.id_'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id_'), nullable=False)

    user = relationship('User', back_populates='session_players')


    def __repr__(self):
        return f"Session(id_={self.id_}, game_id='{self.game_id}' , master_id='{self.master_id}'"
