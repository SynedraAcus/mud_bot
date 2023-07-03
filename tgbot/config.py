from dataclasses import dataclass
from os import getenv


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: str


@dataclass
class RedisConfig:
    host: str
    password: str
    port: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig
    misc: Miscellaneous


def load_config():
    return Config(
        tg_bot=TgBot(
            token=getenv("BOT_TOKEN"),
            admin_ids=list(map(int, getenv("ADMINS").split(","))),
            use_redis=bool(getenv("USE_REDIS")),
        ),
        db=DbConfig(
            host=getenv("POSTGRES_HOST"),
            password=getenv("POSTGRES_PASSWORD"),
            user=getenv("POSTGRES_USER"),
            database=getenv("POSTGRES_DB"),
            port=getenv("POSTGRES_PORT"),
        ),
        redis=RedisConfig(
            host=getenv("REDIS_HOST"),
            password=getenv("REDIS_PWD"),
            port=getenv("REDIS_PORT"),
        ),
        misc=Miscellaneous(),
    )


config = load_config()
