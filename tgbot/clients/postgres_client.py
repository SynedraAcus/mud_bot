"""
PostgreSQL client
"""
import random

from psycopg2 import connect

from tgbot.config import config
from tgbot.misc.metaclasses import SingletonMeta
from tgbot.world.scene import Action, Check, Command, Scene


class PostgresClient(metaclass=SingletonMeta):
    def __init__(self):
        self._config = config.db
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


class PSQLSceneStorage(PostgresClient, metaclass=SingletonMeta):
    @staticmethod
    def _build_action(row):
        """
        Build a command instance out of row returned by SQL request
        :param row:
        :return:
        """
        action = Action(
            keywords=row[0].split(";"),
            description_success=row[1],
            description_failure=row[2],
        )
        if row[3]:
            # THere is a check
            action.check = Check(
                check_type=row[3], variable=row[7], compare_against=row[8]
            )
        if row[6]:
            # There is a command
            action.command = Command(command=row[6], variable=row[4], value=row[5])
        return action

    @staticmethod
    def _build_additional(row):
        """
        Build an Additional instance (Check & text tuple) out of row returned
        by the SQL request
        :param row:
        :return:
        """
        return (
            Check(check_type=row[0], variable=row[1], compare_against=row[2]),
            row[3],
        )

    def get_scene_by_id(self, scene_id: str):
        self._cursor.execute(
            f"SELECT scene_id, description FROM scenes WHERE scene_identifier='{scene_id}'"  # noqa:E501
        )
        psql_id, description = self._cursor.fetchall()[0]
        scene = Scene(scene_id=scene_id, description=description)
        self._cursor.execute(
            f"""SELECT keywords, description_s, description_f, check_type,
commands.variable as command_variable, new_value, command_type,
checks.variable as check_variable, compare_against
FROM actions
LEFT JOIN checks ON actions.check_id = checks.check_id
LEFT JOIN commands ON commands.action_id = actions.action_id
WHERE scene_id={psql_id}"""
        )
        # Process this stuff
        actions = []
        for row in self._cursor.fetchall():
            actions.append(self._build_action(row))
        scene.actions = actions
        # Load additionals
        self._cursor.execute(
            f"""
SELECT check_type, variable, compare_against, additional_text FROM additionals
JOIN checks ON additionals.check_id = checks.check_id
WHERE scene_id = {psql_id}"""
        )
        additionals = []
        for row in self._cursor.fetchall():
            additionals.append(self._build_additional(row))
        scene.additional_descs = additionals
        return scene
