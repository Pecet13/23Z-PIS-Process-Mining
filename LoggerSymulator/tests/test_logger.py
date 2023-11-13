from src.my_database_client import DatabaseClient
from src.logger import Logger

def test_logger():
    # Create a mock database client
    db_client = DatabaseClient()

    # Create a logger instance
    logger = Logger(db_client)

    # Log some data
    logger.log("Test log message")

    # Send logs to database
    logger.send_logs_to_database()

    # Check that the logs were sent successfully
    assert db_client.get_logs() == ["Test log message"]

