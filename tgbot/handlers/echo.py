from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from tgbot.clients.postgres_client import PostgresClient


async def bot_echo(message: types.Message):
    text = ["Эхо без состояния.", "Сообщение:", message.text]

    await message.answer("\n".join(text))


async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f"Эхо в состоянии {hcode(state_name)}",
        "Содержание сообщения:",
        hcode(message.text),
    ]
    await message.answer("\n".join(text))


async def custom_echo(message: types.Message):
    text = f"Here's what you said: {message.text}"
    await message.answer(text)


async def placeholder(message: types.Message):
    client = PostgresClient()  # Assumes that this object is a singleton
    await message.answer(client.get_random_placeholder())


def register_echo(dp: Dispatcher):
    dp.register_message_handler(custom_echo, commands="echo")
    dp.register_message_handler(placeholder, commands="placeholder")
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(
        bot_echo_all, state="*", content_types=types.ContentTypes.ANY
    )
