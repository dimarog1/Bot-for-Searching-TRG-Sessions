from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', age='{self.age}')"
