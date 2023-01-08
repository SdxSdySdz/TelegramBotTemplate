from aiogram import types

from core.handlers import CommandHandler, PureHandler


class EchoHandler(PureHandler):
    async def _handle(self, message: types.Message):
        text = [
            "Эхо без состояния.",
            "Сообщение:",
            message.text
        ]

        await message.answer('\n'.join(text))


class CommandStartHandler(CommandHandler):
    @property
    def command(self):
        return "start"

    async def _handle(self, message: types.Message):
        await message.reply("Hello, user!")
