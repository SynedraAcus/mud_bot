from redis import Redis

from tgbot.config import config
from tgbot.misc.metaclasses import SingletonMeta


class RedisClient(metaclass=SingletonMeta):
    """
    Placeholder Redis client

    This one is only used for placeholder. Actual storage of players' data is to
    be implemented via aiogram.FSM
    """

    def __init__(self):
        self._config = config.redis
        self.connection = Redis(
            host=self._config.host,
            password=self._config.password,
            port=self._config.port,
            decode_responses=True,
        )

    def get_placeholder(self):
        return self.connection.get("test_line")
