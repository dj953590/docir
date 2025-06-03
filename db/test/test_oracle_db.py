import pytest
import oracledb
from unittest.mock import call, MagicMock
from sqlalchemy import text
from db.exceptions import ConnectionError, QueryExecutionError, RetryExhaustedError

@pytest.mark.asyncio
async def test_initialization(oracle_db, mock_engine):
    assert oracle_db.engine is not None
    assert oracle_db.async_session is not None

@pytest.mark.asyncio
async def test_execute_success(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(return_value=MagicMock(rowcount=1))
    query = "SELECT 1 FROM DUAL"

    # Execute
    result = await oracle_db.execute(query)

    # Verify
    assert result == 1
    mock_async_session.execute.assert_awaited_once_with(text(query), {})
    mock_async_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_execute_with_params(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(return_value=MagicMock(rowcount=1))
    query = "INSERT INTO users VALUES (:id, :name)"
    params = {"id": 1, "name": "John"}

    # Execute
    result = await oracle_db.execute(query, params)

    # Verify
    assert result == 1
    mock_async_session.execute.assert_awaited_once_with(text(query), params)

@pytest.mark.asyncio
async def test_execute_fetch(oracle_db, mock_async_session):
    # Setup
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [{"id": 1}]
    mock_async_session.execute = AsyncMock(return_value=mock_result)
    query = "SELECT * FROM users"

    # Execute
    result = await oracle_db.execute(query, fetch=True)

    # Verify
    assert result == [{"id": 1}]

@pytest.mark.asyncio
async def test_fetch_all(oracle_db, mock_async_session):
    # Setup
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [{"id": 1}, {"id": 2}]
    mock_async_session.execute = AsyncMock(return_value=mock_result)
    query = "SELECT * FROM users"

    # Execute
    result = await oracle_db.fetch_all(query)

    # Verify
    assert result == [{"id": 1}, {"id": 2}]

@pytest.mark.asyncio
async def test_fetch_one(oracle_db, mock_async_session):
    # Setup
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = [{"id": 1}]
    mock_async_session.execute = AsyncMock(return_value=mock_result)
    query = "SELECT * FROM users WHERE id = :id"
    params = {"id": 1}

    # Execute
    result = await oracle_db.fetch_one(query, params)

    # Verify
    assert result == {"id": 1}

@pytest.mark.asyncio
async def test_fetch_one_no_results(oracle_db, mock_async_session):
    # Setup
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []
    mock_async_session.execute = AsyncMock(return_value=mock_result)

    # Execute
    result = await oracle_db.fetch_one("SELECT * FROM empty_table")

    # Verify
    assert result is None

@pytest.mark.asyncio
async def test_execute_many(oracle_db, mock_async_session):
    # Setup
    query = "INSERT INTO users VALUES (:id, :name)"
    params_list = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]

    # Execute
    await oracle_db.execute_many(query, params_list)

    # Verify
    mock_async_session.execute.assert_awaited_once_with(text(query), params_list)
    mock_async_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_retry_on_connection_error(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(side_effect=[
        oracledb.DatabaseError(MagicMock(code=3113)),
        MagicMock(rowcount=1)
    ])

    # Execute
    result = await oracle_db.execute("SELECT 1 FROM DUAL")

    # Verify
    assert result == 1
    assert mock_async_session.execute.call_count == 2

@pytest.mark.asyncio
async def test_retry_exhausted(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(
        side_effect=oracledb.DatabaseError(MagicMock(code=3113))
    )

    # Execute and verify exception
    with pytest.raises(RetryExhaustedError):
        await oracle_db.execute("SELECT 1 FROM DUAL")

    # Verify retry attempts (default 3 retries = 4 total attempts)
    assert mock_async_session.execute.call_count == 4

@pytest.mark.asyncio
async def test_non_retryable_error(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(
        side_effect=oracledb.DatabaseError(MagicMock(code=942))  # Table does not exist
    )

    # Execute and verify exception
    with pytest.raises(QueryExecutionError):
        await oracle_db.execute("SELECT * FROM non_existent_table")

    # Verify only one attempt
    assert mock_async_session.execute.call_count == 1

@pytest.mark.asyncio
async def test_unexpected_exception(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(side_effect=ValueError("Unexpected"))

    # Execute and verify exception
    with pytest.raises(QueryExecutionError):
        await oracle_db.execute("SELECT 1 FROM DUAL")

@pytest.mark.asyncio
async def test_close(oracle_db, mock_engine):
    # Execute
    await oracle_db.close()

    # Verify
    mock_engine.dispose.assert_awaited_once()

@pytest.mark.asyncio
async def test_transaction_success(oracle_db, mock_async_session):
    # Setup
    async with oracle_db.transaction() as session:
        await session.execute(text("UPDATE users SET name = 'John' WHERE id = 1"))

    # Verify
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_transaction_rollback(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(side_effect=Exception("Boom"))

    # Execute
    with pytest.raises(Exception):
        async with oracle_db.transaction() as session:
            await session.execute(text("INVALID SQL"))

    # Verify
    mock_async_session.rollback.assert_awaited_once()
    mock_async_session.commit.assert_not_called()
    mock_async_session.close.assert_awaited_once()

@pytest.mark.asyncio
async def test_query_logging(oracle_db, mock_async_session, caplog):
    # Setup
    oracle_db.log_params = True
    query = "SELECT * FROM users WHERE id = :id"
    params = {"id": 1}

    # Execute
    await oracle_db.execute(query, params)

    # Verify logging
    assert "Executing query:" in caplog.text
    assert query in caplog.text
    assert "Parameters: {'id': 1}" in caplog.text

@pytest.mark.asyncio
async def test_logging_without_params(oracle_db, mock_async_session, caplog):
    # Setup
    oracle_db.log_params = False
    query = "SELECT * FROM sensitive_table"
    params = {"token": "secret"}

    # Execute
    await oracle_db.execute(query, params)

    # Verify logging
    assert "Executing query:" in caplog.text
    assert query in caplog.text
    assert "token" not in caplog.text
    assert "secret" not in caplog.text

@pytest.mark.asyncio
async def test_connection_error_codes(oracle_db, mock_async_session):
    # Test all connection-related error codes
    connection_codes = [28, 1013, 1033, 1034, 1089, 3113, 3114, 3135]

    for code in connection_codes:
        mock_async_session.execute = AsyncMock(
            side_effect=oracledb.DatabaseError(MagicMock(code=code))
        )

        with pytest.raises(ConnectionError):
            await oracle_db.execute("SELECT 1 FROM DUAL")

@pytest.mark.asyncio
async def test_non_connection_error_codes(oracle_db, mock_async_session):
    # Test non-connection error codes
    mock_async_session.execute = AsyncMock(
        side_effect=oracledb.DatabaseError(MagicMock(code=942))  # Table not found
    )

    with pytest.raises(QueryExecutionError):
        await oracle_db.execute("SELECT * FROM missing_table")

@pytest.mark.asyncio
async def test_init_with_sid(oracle_db, monkeypatch, mock_engine):
    # Setup
    monkeypatch.setattr(
        "sqlalchemy.ext.asyncio.create_async_engine",
        MagicMock(return_value=mock_engine)
    )

    # Execute
    from db.oracle import OracleDB
    db = OracleDB(
        username="test",
        password="test",
        host="localhost",
        sid="XE"
    )

    # Verify
    assert db.engine is not None

@pytest.mark.asyncio
async def test_init_missing_service_and_sid():
    # Execute and verify
    from db.oracle import OracleDB
    with pytest.raises(ValueError):
        OracleDB(
            username="test",
            password="test",
            host="localhost"
        )

@pytest.mark.asyncio
async def test_execute_many_error(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(
        side_effect=oracledb.DatabaseError(MagicMock(code=3113))
    )

    # Execute and verify
    with pytest.raises(RetryExhaustedError):
        await oracle_db.execute_many(
            "INSERT INTO users VALUES (:id)",
            [{"id": 1}, {"id": 2}]
        )

@pytest.mark.asyncio
async def test_session_commit_failure(oracle_db, mock_async_session):
    # Setup
    mock_async_session.commit = AsyncMock(side_effect=Exception("Commit failed"))

    # Execute and verify
    with pytest.raises(QueryExecutionError):
        await oracle_db.execute("SELECT 1 FROM DUAL")

@pytest.mark.asyncio
async def test_session_rollback(oracle_db, mock_async_session):
    # Setup
    mock_async_session.execute = AsyncMock(side_effect=Exception("Query failed"))

    # Execute and verify
    with pytest.raises(QueryExecutionError):
        await oracle_db.execute("INVALID SQL")

    # Verify rollback was called
    mock_async_session.rollback.assert_awaited_once()