"""
Main classes responsible for Scene
"""
from abc import ABC
from dataclasses import dataclass, field
from enum import Enum


class CommandType(str, Enum):
    """
    A enum of valid command types
    """

    set_var = "set_var"
    change_var = "change_var"
    set_scene = "set_scene"


# Not using Pydantic because its validation breaks in a weird way on Cyrillic-ru
@dataclass
class Command:
    """
    A command that Scene emits when interacted with.

    Should somehow affect player state
    """

    command: CommandType
    value: str | int | bool
    variable: str | None = None


class CheckType(str, Enum):
    equals = "equals"
    more = "more"
    more_or_equal = "more_or_equal"
    less = "less"
    less_or_equal = ("less_or_equal",)
    exists = "exists"
    not_exists = "not_exists"


@dataclass
class Check:
    """
    A check on player variable
    """

    check_type: CheckType
    variable: str
    compare_against: str | None = None


@dataclass
class Action:
    """
    An action that player can perform in the scene
    """

    keywords: list[str | bytes]
    command: Command | None = None  # What happens in case of success
    check: Check | None = None
    description_success: str | bytes = ""  # Text if successful
    description_failure: str | bytes = ""  # Text if failed


@dataclass()
class Scene:
    """
    A Scene containing a description, an optional list of additional descs,
    and possible actions. It may also contain Commands that are executed on a
    check upon entering the scene
    """

    scene_id: str
    description: str
    actions: list[Action] = field(default_factory=list)
    additional_descs: list[tuple[Check, str]] = field(default_factory=list)


class SceneStorageInterface(ABC):
    """
    Returns scenes by ID
    """

    def get_scene_by_id(self, scene: str) -> Scene:
        pass
