from tgbot.clients.redis_client import RedisClient
from tgbot.world.scene import (
    Action,
    Check,
    Command,
    CommandType,
    SceneStorageInterface,
)


class RedisEngine:
    """
    Single-player engine for testing in the console
    """

    def __init__(self, storage, starting_scene: str = "start"):
        self.starting_scene = starting_scene
        self.storage = storage
        self.command_overrides = {
            "scene": self.print_scene,
            "vars": self.print_vars,
            "restart": self.start,
            "о": self.show,
            "осмотреться": self.show,
        }

    def start(self, player_id: int) -> None:
        r_conn = RedisClient()
        r_conn.wipe(player_id)
        r_conn.set_scene(player_id, self.starting_scene)
        # No other vars need to init so far, but remove old ones in case it is
        # a restart
        return ""  # In case it was called via bot

    def set_scene(self, player_id: int, scene_id: str) -> None:
        """
        Set the scene to what is requested
        :return:
        """
        RedisClient().set_scene(player_id=player_id, scene_id=scene_id)

    def evaluate_check(self, player_id: int, check: Check) -> bool:
        """
        Evaluate a check using variables in self.vars
        :param check:
        :return:
        """
        r_conn = RedisClient()
        exists = r_conn.exists(player_id=player_id, varname=check.variable)
        if check.check_type == "exists":
            return exists
        elif check.check_type == "not_exists":
            return not exists
        if not exists:
            # Fail all comparison checks for variables that were not set
            return False
        check_lambdas = {
            "equals": lambda a, b: a == b,
            "more": lambda a, b: a > b,
            "more_or_equal": lambda a, b: a >= b,
            "less": lambda a, b: a < b,
            "less_or_equal": lambda a, b: a <= b,
        }
        val = r_conn.get(player_id=player_id, varname=check.variable)
        if "more" in check.check_type or "less" in check.check_type:
            # Only defined on ints, casting both just in case
            return check_lambdas[check.check_type](int(val), int(check.compare_against))
        else:
            return check_lambdas[check.check_type](val, check.compare_against)

    def execute_action(self, player_id: int, action: Action) -> str | None:
        if action.check:
            if not self.evaluate_check(player_id=player_id, check=action.check):
                return action.description_failure
        if action.command:
            self.execute_command(player_id=player_id, command=action.command)
            return action.description_success

    def execute_command(self, player_id: int, command: Command) -> None:
        if command.command == CommandType.set_scene:
            self.set_scene(player_id, command.value)
        elif command.command == CommandType.set_var:
            RedisClient().set(
                player_id=player_id, varname=command.variable, value=command.value
            )
        elif command.command == CommandType.change_var:
            # Only works on ints
            val = int(RedisClient().get(player_id, command.variable)) + int(
                command.value
            )
            RedisClient().set(player_id, command.variable, val)

    async def process_input(self, player_id: int, player_input: str):
        """
        Execute player command in current scene
        """
        c = player_input.rstrip().lower()
        if c in self.command_overrides:
            return self.command_overrides[c](player_id)
        else:
            scene_id = RedisClient().get_scene(player_id)
            if not scene_id:
                # Gets None, but doesn't throw exception iff this is literally
                # the first time player enters the bot.
                self.start(player_id)
                scene_id = self.starting_scene
            scene = self.storage.get_scene_by_id(scene_id)
            for action in scene.actions:
                if c in action.keywords:
                    res = self.execute_action(player_id, action)
                    if not res:
                        return ""
                    return res
            return f'Я не понял команду "{c}"'

    async def show(self, player_id):
        """
        Display the current scene
        """
        scene_id = RedisClient().get_scene(player_id)
        scene = self.storage.get_scene_by_id(scene_id)
        r = scene.description
        if len(scene.additional_descs) > 0:
            for check, desc in scene.additional_descs:
                if self.evaluate_check(player_id, check):
                    r += "\n" + desc
        return r

    # Command overrides for debugging
    def print_scene(self, player_id: int):
        return RedisClient().get_scene(player_id)

    def print_vars(self, player_id: int):
        return str(RedisClient().all_vars(player_id))


# TODO: create a superclass for SPEngine and RedisEngine
# TODO: fix SP engine, remove Redis bits and pieces
class SPEngine:
    """
    Single-player engine for testing in the console
    """

    def __init__(self, storage: SceneStorageInterface, starting_scene: str = "start"):
        self.vars = dict()
        self.starting_scene = starting_scene
        self._current_scene = starting_scene
        self.storage = storage
        self.command_overrides = {
            "scene": self.print_scene,
            "vars": self.print_vars,
            "restart": self.start,
            "о": self.show,
            "осмотреться": self.show,
        }

    def start(self, player_id: int) -> str:
        redis_conn = RedisClient()
        return redis_conn.set_scene(player_id, self.starting_scene)

    def set_scene(self, player_id: int, scene_id: str) -> str:
        """
        Set the scene to what is requested
        :return:
        """
        redis_conn = RedisEngine()
        redis_conn.set_scene(player_id, scene_id)
        return self.show()

    def evaluate_check(self, check: Check):
        """
        Evaluate a check using variables in self.vars
        :param check:
        :return:
        """
        RedisEngine()
        if check.check_type == "exists":
            pass
        elif check.check_type == "not_exists":
            return check.variable not in self.vars
        if check.variable not in self.vars:
            # Fail all comparison checks for variables that were not set
            return False
        check_lambdas = {
            "equals": lambda a, b: a == b,
            "more": lambda a, b: a > b,
            "more_or_equal": lambda a, b: a >= b,
            "less": lambda a, b: a < b,
            "less_or_equal": lambda a, b: a <= b,
        }
        if "more" in check.check_type or "less" in check.check_type:
            # Only defined on ints, casting both just in case
            return check_lambdas[check.check_type](
                int(self.vars[check.variable]), int(check.compare_against)
            )
        else:
            return check_lambdas[check.check_type](
                self.vars[check.variable], check.compare_against
            )

    def execute_action(self, action: Action):
        if action.check:
            if not self.evaluate_check(action.check):
                print(action.description_failure)
                return
            print(action.description_success)
        if action.command:
            self.execute_command(action.command)

    def execute_command(self, command: Command):
        if command.command == CommandType.set_scene:
            self.set_scene(command.value)
        elif command.command == CommandType.set_var:
            self.vars[command.variable] = command.value
        elif command.command == CommandType.change_var:
            # Only works on ints
            self.vars[command.variable] = int(self.vars[command.variable])
            self.vars[command.variable] += int(command.value)

    def process_input(self, player_input: str):
        """
        Execute player command in current scene
        :param input:
        :return:
        """
        c = player_input.rstrip().lower()
        if c in self.command_overrides:
            self.command_overrides[c]()
        else:
            has_processed = False
            for action in self._current_scene.actions:
                if c in action.keywords:
                    self.execute_action(action)
                    has_processed = True
            if not has_processed:
                print(f'Я не понял команду "{c}"')

    def show(self):
        """
        Display the current scene
        :return:
        """
        print(self._current_scene.description)
        if len(self._current_scene.additional_descs) > 0:
            for check, desc in self._current_scene.additional_descs:
                if self.evaluate_check(check):
                    print(desc)

    # Command overrides for debugging
    def print_scene(self):
        print(self._current_scene.scene_id)

    def print_vars(self):
        print(self.vars)
