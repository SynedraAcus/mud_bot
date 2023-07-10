#! python3.10

"""
A singleplayer engine for testing
"""
from tgbot.world.scene import Action, Check, Command, CommandType
from tgbot.world.test_scenes import TestStorage


class Engine:
    """
    Single-player engine for testing in the console
    """

    def __init__(self, starting_scene: str = "start"):
        self.vars = dict()
        self._current_scene = None
        self.starting_scene = starting_scene
        self.storage = TestStorage()
        self.command_overrides = {
            "scene": self.print_scene,
            "vars": self.print_vars,
            "restart": self.start,
            "о": self.show,
            "осмотреться": self.show,
        }
        self.start()

    def start(self):
        self.vars = dict()
        self.set_scene(self.starting_scene)

    def set_scene(self, scene_id: str):
        """
        Set the scene to what is requested
        :return:
        """
        self._current_scene = self.storage.get_scene_by_id(scene_id)
        if len(self._current_scene.auto_executed) > 0:
            for check, command in self._current_scene.auto_executed:
                if self.evaluate_check(check):
                    self.execute_command()
        self.show()

    def evaluate_check(self, check: Check):
        """
        Evaluate a check using variables in self.vars
        :param check:
        :return:
        """
        if check.check_type == "exists":
            return check.variable in self.vars
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


if __name__ == "__main__":
    e = Engine()
    while True:
        e.process_input(input(">"))
