class DatabaseError(Exception):
    """Base database exception"""

class ConnectionError(DatabaseError):
    """Connection-related errors"""

class QueryExecutionError(DatabaseError):
    """Query execution errors"""

class RetryExhaustedError(DatabaseError):
    """All retry attempts exhausted"""