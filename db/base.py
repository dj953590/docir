import logging
from abc import ABC
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, List, Optional, Tuple, Union

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .exceptions import DatabaseError, ConnectionError, QueryExecutionError
from .utils import with_retry

logger = logging.getLogger(__name__)

class AsyncDB(ABC):
    """Base class for all database implementations"""
    def __init__(
            self,
            dsn: str,
            *,
            max_retries: int = 3,
            log_queries: bool = True,
            log_params: bool = False,
            **engine_kwargs
    ):
        self.dsn = dsn
        self.max_retries = max_retries
        self.log_queries = log_queries
        self.log_params = log_params
        self.engine = create_async_engine(dsn, **engine_kwargs)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    def _log_query(self, query: str, params: Any = None) -> None:
        """Log query with optional parameters"""
        if not self.log_queries:
            return

        log_message = f"Executing query:\n{query}"

        if self.log_params and params:
            log_message += f"\nParameters: {params}"

        logger.debug(log_message)

    def _handle_exception(self, e: Exception) -> None:
        """Database-specific exception handling (to be implemented by subclasses)"""
        raise NotImplementedError

    @with_retry
    async def execute(
            self,
            query: str,
            params: Optional[Union[Dict, List, Tuple]] = None,
            fetch: bool = False
    ) -> Any:
        self._log_query(query, params)

        try:
            async with self.async_session() as session:
                result = await session.execute(text(query), params or {})
                if fetch:
                    return result.mappings().all()
                await session.commit()
                return result.rowcount
        except Exception as e:
            self._handle_exception(e)

    @with_retry
    async def execute_many(
            self,
            query: str,
            params_list: List[Union[Dict, List, Tuple]]
    ) -> None:
        self._log_query(query, params_list)

        try:
            async with self.async_session() as session:
                stmt = text(query)
                await session.execute(stmt, params_list)
                await session.commit()
        except Exception as e:
            self._handle_exception(e)

    async def fetch_all(
            self,
            query: str,
            params: Optional[Union[Dict, List, Tuple]] = None
    ) -> List[Dict]:
        result = await self.execute(query, params, fetch=True)
        return result

    async def fetch_one(
            self,
            query: str,
            params: Optional[Union[Dict, List, Tuple]] = None
    ) -> Optional[Dict]:
        result = await self.fetch_all(query, params)
        return result[0] if result else None

    async def close(self) -> None:
        if self.engine:
            await self.engine.dispose()

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator:
        """Context manager for transactional operations"""
        session = self.async_session()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Transaction rolled back: {str(e)}")
            raise
        finally:
            await session.close()