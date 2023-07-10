"""
A bunch of Scene instances created for the testing
"""

from tgbot.world.scene import (
    Action,
    Check,
    CheckType,
    Command,
    CommandType,
    Scene,
    SceneStorageInterface,
)

starter_scene = Scene(
    scene_id="start",
    description="Вы стоите в коридоре, простирающемся с севера на юг.",
    actions=[
        Action(
            keywords=["ю", "юг"],
            command=Command(command=CommandType.set_scene, value="south"),
        ),
        Action(
            keywords=["с", "север"],
            command=Command(command=CommandType.set_scene, value="north"),
        ),
    ],
)


north_scene = Scene(
    scene_id="north",
    description="Вы стоите в северном конце коридора.",
    additional_descs=[
        (
            Check(check_type=CheckType.not_exists, variable="has_crowbar"),
            "На полу валяется монтировка. Пригодится на случай встречи с хэдкрабами или запертыми дверями.",  # noqa:E501
        )
    ],  # noqa: E501
    actions=[
        Action(
            keywords=["ю", "юг"],
            command=Command(command=CommandType.set_scene, value="start"),
        ),
        Action(
            keywords=["с", "север"],
            check=Check(
                check_type=CheckType.more_or_equal,
                variable="Nonexistent",
                compare_against=10,
            ),
            description_failure="На то он и северный конец, что дальше на север идти нельзя.",  # noqa:E501
        ),
        Action(
            keywords=["взять", "забрать", "подобрать"],
            check=Check(check_type=CheckType.not_exists, variable="has_crowbar"),
            command=Command(
                command=CommandType.set_var, variable="has_crowbar", value=True
            ),
            description_failure="Брать тут больше нечего.",
            description_success="Вы берёте монтировку в руку и сразу чувствуете себя увереннее.",  # noqa:E501
        ),
    ],
)

south_scene = Scene(
    scene_id="south",
    description="Вы стоите в южном конце коридора. Потолок перекошен, а чуть южнее проход вообще завален.",  # noqa:E501
    actions=[
        Action(
            keywords=["с", "север"],
            command=Command(command=CommandType.set_scene, value="start"),
        ),
        Action(
            keywords=["ю", "юг"],
            command=Command(command=CommandType.set_scene, value="rocks"),
        ),
    ],
)

rocks_scene = Scene(
    scene_id="rocks",
    description="Коридор завален камнями и бетонными плитами.",
    additional_descs=[
        (
            Check(
                variable="cleared_rocks",
                check_type=CheckType.equals,
                compare_against=True,
            ),
            "Под одной из плит виднеется узкий лаз.",
        ),
        (
            Check(variable="cleared_rocks", check_type=CheckType.not_exists),
            "Кажется, если их не убрать — пройти не получится.",
        ),
    ],
    actions=[
        Action(
            keywords=["убрать", "очистить", "расчистить"],
            check=Check(
                variable="has_crowbar",
                check_type=CheckType.equals,
                compare_against=True,
            ),
            command=Command(
                command=CommandType.set_var, variable="cleared_rocks", value=True
            ),
            description_success="Вам удалось отвалить несколько камней, и теперь тут можно пролезть.",  # noqa:E501
            description_failure="Голыми руками их точно не сдвинуть с места.",
        ),
        Action(
            keywords=["с", "север"],
            command=Command(command=CommandType.set_scene, value="south"),
        ),
        Action(
            keywords=["ю", "юг"],
            check=Check(
                variable="cleared_rocks",
                check_type=CheckType.equals,
                compare_against=True,
            ),
            command=Command(command=CommandType.set_scene, value="final"),
            description_failure="Коридор всё ещё завален, и пройти тут нельзя.",
            description_success="Обдирая колени, вы пролазите под плитой.",
        ),
    ],
)

final_scene = Scene(
    scene_id="Final",
    description="К сожалению, нормальное количество контента будет добавлено когда-нибудь потом. На данный момент это конец.",  # noqa:E501
)


class TestStorage(SceneStorageInterface):
    def __init__(self):
        self.scenes = [
            starter_scene,
            north_scene,
            south_scene,
            rocks_scene,
            final_scene,
        ]

    def get_scene_by_id(self, scene: str) -> Scene:
        for x in self.scenes:
            if x.scene_id == scene:
                return x
        raise KeyError(f"Requesting nonexistent scene {scene}")
