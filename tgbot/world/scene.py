"""
Main classes responsible for Scene
"""
from abc import ABC
from enum import Enum

from pydantic import BaseModel


class CommandType(str, Enum):
    """
    A enum of valid command types
    """

    set_var = "set_var"
    change_var = "change_var"
    set_scene = "set_scene"


class Command(BaseModel):
    """
    A command that Scene emits when interacted with.

    Should somehow affect player state
    """

    command: CommandType
    variable: str | None = None
    value: str | int | bool


class CheckType(str, Enum):
    equals = "equals"
    more = "more"
    more_or_equal = "more_or_equal"
    less = "less"
    less_or_equal = ("less_or_equal",)
    exists = "exists"
    not_exists = "not_exists"


class Check(BaseModel):
    """
    A check on player variable
    """

    check_type: CheckType
    variable: str
    compare_against: str | int | bool | None = None  # May be none for 'exists'


# @dataclass
class Action(BaseModel):
    """
    An action that player can perform in the scene
    """

    keywords: list[str | bytes]
    command: Command | None = None  # What happens in case of success
    check: Check | None = None
    description_success: str | bytes = ""  # Text if successful
    description_failure: str | bytes = ""  # Text if failed


class Scene(BaseModel):
    """
    A Scene containing a description, an optional list of additional descs,
    and possible actions. It may also contain Commands that are executed on a
    check upon entering the scene
    """

    scene_id: str
    description: str
    additional_descs: list[tuple[Check, str]] = []
    auto_executed: list[tuple[Check, Command]] = []
    actions: list[Action]  # Scene should have at least 1 action for exiting it


class SceneStorageInterface(ABC):
    """
    Returns scenes by ID
    """

    def __init__(self):
        pass

    def get_scene_by_id(self, scene: str) -> Scene:
        pass
