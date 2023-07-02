from aiogram import types, Dispatcher
from tgbot.clients.postgres_client import PostgresClient
from tgbot.clients.redis_client import RedisClient


async def custom_echo(message: types.Message):
    text = f"Here's what you said: {message.text}"
    await message.answer(text)


async def postrges_placeholder(message: types.Message):
    client = PostgresClient()  # Assumes that this object is a singleton
    await message.answer(client.get_random_placeholder())


async def redis_placeholder(message: types.Message):
    client = RedisClient()
    await message.answer(client.get_placeholder())


def register_echo(dp: Dispatcher):
    dp.register_message_handler(custom_echo, commands="echo")
    dp.register_message_handler(postrges_placeholder, commands="placeholder")
    dp.register_message_handler(redis_placeholder, commands="redis")
