from aiogram import Dispatcher
from aiogram.types import ContentType, Message

from tgbot.clients.postgres_client import PSQLSceneStorage
from tgbot.engines.engines import RedisEngine

engine = RedisEngine(storage=PSQLSceneStorage())


async def user_start(message: Message):
    await message.reply("Hello, user!")


# TODO: send short intro upon registration, set correct user state


async def process_message(message: Message):
    user_id = message.from_user.id
    user_input = message.text
    if user_input[0] == "/":
        # Crude command excluder, because I can't figure out negative filters
        return
    reply_text = ""
    reply_text += (
        await engine.process_input(user_id, user_input)
        + "\n\n"
        + await engine.show(user_id)
    )
    await message.reply(reply_text)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(process_message, content_types=ContentType.all())
