import oracledb
from .base import AsyncDB
from .exceptions import ConnectionError, QueryExecutionError

class OracleDB(AsyncDB):
    def __init__(
            self,
            username: str,
            password: str,
            host: str,
            port: int = 1521,
            service_name: str = None,
            sid: str = None,
            **kwargs
    ):
        if not service_name and not sid:
            raise ValueError("Either service_name or sid must be provided")

        # Create DSN
        dsn = f"{host}:{port}/"
        dsn += service_name if service_name else sid

        # Create connection string
        conn_str = f"oracle+oracledb://{username}:{password}@{dsn}"

        super().__init__(conn_str, **kwargs)

    def _handle_exception(self, e: Exception) -> None:
        if isinstance(e, oracledb.DatabaseError):
            error = e.args[0]
            logger.error(f"Oracle error: {error.code} - {error.message}")
            if error.code in (28, 1013, 1033, 1034, 1089, 3113, 3114, 3135):
                raise ConnectionError from e
            raise QueryExecutionError from e
        logger.exception("Unexpected error during query execution")
        raise DatabaseError from e