from aiogram import Dispatcher, types

from tgbot.clients.postgres_client import PostgresClient
from tgbot.clients.redis_client import RedisClient


async def custom_echo(message: types.Message):
    stripped = message.text[6:]  # filter only sends msgs starting with '/echo '
    text = f"Here's what you said: {stripped}\n(your ID is {message.from_user.id})"  # noqa: E501
    await message.answer(text)


async def postrges_placeholder(message: types.Message):
    client = PostgresClient()  # Assumes that this object is a singleton
    try:
        text = client.get_random_placeholder()
    except Exception as e:
        text = f"Something wrong with postgreSQL:\n{e}"
    await message.answer(text)


async def redis_placeholder(message: types.Message):
    client = RedisClient()
    try:
        text = client.get_placeholder()
        if not text:
            text = "No `test_line` in Redis DB"
    except Exception as e:
        text = f"Something wrong with Redis:\n{e}"
    await message.answer(text)


def register_echo(dp: Dispatcher):
    dp.register_message_handler(custom_echo, commands="echo")
    dp.register_message_handler(postrges_placeholder, commands="postgres")
    dp.register_message_handler(redis_placeholder, commands="redis")
