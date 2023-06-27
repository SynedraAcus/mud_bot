"""
PostgreSQL client
"""
import random

from tgbot.config import load_config
from psycopg2 import connect


class PostgresClient:
    # TODO: make a singleton
    def __init__(self):
        self._config = load_config(".env").db
        self.connection = connect(
            host=self._config.host,
            port=self._config.port,
            password=self._config.password,
            user=self._config.user,
            database=self._config.database,
        )
        self._cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def get_random_placeholder(self):
        placeholder_id = random.randint(1, 3)
        self._cursor.execute(
            f"SELECT description, additional_desc FROM placeholders WHERE placeholder_id={placeholder_id}"  # noqa:E501
        )
        description, additional = self._cursor.fetchall()[0]
        return description + "\n" + additional
