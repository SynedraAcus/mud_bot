from tgbot.misc.metaclasses import SingletonMeta
from tgbot.config import load_config
from redis import Redis


class RedisClient(metaclass=SingletonMeta):
    """
    Placeholder Redis client

    This one is only used for placeholder. Actual storage of players' data is to
    be implemented via aiogram.FSM
    """

    def __init__(self):
        self._config = load_config(".env").redis
        self.connection = Redis(
            host=self._config.host,
            password=self._config.password,
            port=self._config.port,
            decode_responses=True,
        )

    def get_placeholder(self):
        return self.connection.get("test_line")
