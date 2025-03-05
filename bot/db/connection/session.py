from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, ClassVar, Any
import asyncio

from bot.config import get_settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    _instance: ClassVar[Optional['SessionManager']] = None
    _engine: Optional[create_async_engine] = None
    _session_factory: Optional[async_scoped_session] = None

    def __init__(self, **engine_kwargs: Any):
        if SessionManager._instance:
            raise RuntimeError("Use AsyncDatabase.get_session() to get instances")

        self.engine_kwargs = engine_kwargs

        self._engine = None

    async def _initialize(self) -> None:
        """Инициализация внутренних компонентов"""
        self._engine = create_async_engine(
            get_settings().database_uri,
            **self.engine_kwargs
        )
        self._session_factory = async_scoped_session(
            sessionmaker(
                self._engine,
                expire_on_commit=False,
                class_=AsyncSession
            ),
            scopefunc=lambda: id(asyncio.current_task())
        )

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance  # noqa

    def refresh(self) -> None:
        self._engine = create_async_engine(get_settings().database_uri, echo=True, future=True)

    @classmethod
    @asynccontextmanager
    async def get_session(cls, **engine_kwargs: Any) -> AsyncGenerator[AsyncSession, None]:
        """
        Статический метод для получения сессии через контекстный менеджер.
        При первом вызове требуется передача параметров подключения.
        """
        if not cls._instance:
            cls._instance = SessionManager(**engine_kwargs)
            await cls._instance._initialize()
        elif engine_kwargs:
            raise RuntimeError("Database already initialized. Parameters cannot be changed.")

        session = cls._instance._session_factory()

        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
            await cls._instance._session_factory.remove()


__all__ = [
    "SessionManager",
]
