from aiogram import types, Dispatcher
from tgbot.clients.postgres_client import PostgresClient


async def custom_echo(message: types.Message):
    text = f"Here's what you said: {message.text}"
    await message.answer(text)


async def placeholder(message: types.Message):
    client = PostgresClient()  # Assumes that this object is a singleton
    await message.answer(client.get_random_placeholder())


def register_echo(dp: Dispatcher):
    dp.register_message_handler(custom_echo, commands="echo")
    dp.register_message_handler(placeholder, commands="placeholder")
