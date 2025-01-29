from sqlalchemy import Column, Integer, String, Sequence, func
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TEXT, TIMESTAMP, UUID

from bot.db import DeclarativeBase


class User(DeclarativeBase):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
        unique=True,
        doc="Unique id of the string in table",
    )
    name = Column(
        String(50),
        nullable=False
    )
    age = Column(
        Integer,
        nullable=False
    )

    def __repr__(self):
        columns = {column.name: getattr(self, column.name) for column in self.__table__.columns}
        return f'<{self.__tablename__}: {", ".join(map(lambda x: f"{x[0]}={x[1]}", columns.items()))}>'
