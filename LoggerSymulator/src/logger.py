import time
import logging
from typing import List

# TODO: Replace with your database client library
from my_database_client import DatabaseClient

class Logger:
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client
        self.log_buffer = []

    def log(self, data: str):
        self.log_buffer.append(data)

    def send_logs_to_database(self):
        if self.log_buffer:
            self.db_client.send_logs(self.log_buffer)
            self.log_buffer = []

    def run(self):
        while True:
            self.send_logs_to_database()
            time.sleep(600)  # Sleep for 10 minutes
