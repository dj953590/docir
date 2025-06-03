import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

@pytest.fixture
def mock_async_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def mock_engine(mock_async_session):
    engine = MagicMock(spec=AsyncEngine)
    engine.dispose = AsyncMock()
    return engine

@pytest.fixture
def mock_sessionmaker(mock_async_session):
    return MagicMock(return_value=mock_async_session)

@pytest.fixture
def oracle_db(mock_engine, mock_sessionmaker, monkeypatch):
    # Mock SQLAlchemy engine creation
    monkeypatch.setattr(
        "sqlalchemy.ext.asyncio.create_async_engine",
        MagicMock(return_value=mock_engine)
    )

    # Mock sessionmaker
    monkeypatch.setattr(
        "sqlalchemy.orm.sessionmaker",
        MagicMock(return_value=mock_sessionmaker)
    )

    from db.oracle import OracleDB
    return OracleDB(
        username="test",
        password="test",
        host="localhost",
        service_name="ORCL"
    )