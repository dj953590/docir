import asyncpg
from sqlalchemy.exc import DBAPIError
from .base import AsyncDB
from .exceptions import ConnectionError, QueryExecutionError

class PostgresDB(AsyncDB):
    def __init__(
            self,
            username: str,
            password: str,
            host: str,
            port: int = 5432,
            database: str = "postgres",
            **kwargs
    ):
        # Create connection string
        conn_str = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        super().__init__(conn_str, **kwargs)

    def _handle_exception(self, e: Exception) -> None:
        if isinstance(e, DBAPIError) and isinstance(e.orig, asyncpg.PostgresError):
            pg_error = e.orig
            logger.error(f"PostgreSQL error: {pg_error.code} - {pg_error.message}")

            # Connection-related error codes
            connection_errors = [
                '08000', '08001', '08003', '08004', '08006', '08007',
                '08P01', '57P01', '57P02', '57P03', '58P01'
            ]

            if pg_error.code in connection_errors:
                raise ConnectionError from e
            raise QueryExecutionError from e
        logger.exception("Unexpected error during query execution")
        raise DatabaseError from e