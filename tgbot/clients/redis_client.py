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
        self.reserved_varnames = ("scene", "forbidden")
        self._config = config.redis
        self.connection = Redis(
            host=self._config.host,
            password=self._config.password,
            port=self._config.port,
            decode_responses=True,
        )

    def get_placeholder(self):
        return self.connection.get("test_line")

    @staticmethod
    def _key_name(player_id: int, varname: str) -> str:
        return f"{player_id}:{varname}"

    def set(self, player_id: int, varname: str, value) -> None:
        """
        Saves variable for a player.

        Uses format '{player_id}:var_name'
        """
        if varname in self.reserved_varnames:
            raise ValueError("Forbidden variable name {varname}")
        self.connection.set(self._key_name(player_id, varname), value)

    def exists(self, player_id: int, varname: str) -> bool:
        """
        Returns True iff the variable has previously been set for a player
        """
        # For some reason redis returns int instead of bool
        return self.connection.exists(self._key_name(player_id, varname)) == 1

    def get(self, player_id: int, varname: str):
        return self.connection.get(self._key_name(player_id, varname))

    def get_scene(self, player_id: int):
        """
        Return the scene in which the player currently is.

        Technically, it's just another str variable, but it is reserved and not
        available through regular get/set methods to avoid accidentally
        teleporting people
        """
        return self.connection.get(self._key_name(player_id, "scene"))

    def set_scene(self, player_id: int, scene_id: str):
        # TODO: assert that only existing scenes can be set
        self.connection.set(self._key_name(player_id, "scene"), scene_id)

    def wipe(self, player_id: int):
        """
        Remove all variables related to this player, including reserved ones
        """
        keys = self.connection.keys(f"{player_id}:*")
        for key in keys:
            self.connection.delete(*keys)

    def all_vars(self, player_id: int):
        keys = self.connection.keys(f"{player_id}:*")
        return {x: self.connection.get(x) for x in keys}
