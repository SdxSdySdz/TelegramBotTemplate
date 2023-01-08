from aiogram import types, Dispatcher


class Handler:
    def register_with(self, dispatcher: Dispatcher):
        raise NotImplementedError

    async def _handle(self, message: types.Message):
        raise NotImplementedError()


class PureHandler(Handler):
    def register_with(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self._handle)


class CommandHandler(Handler):
    def __int__(self, command: str):
        self._command = command

    @property
    def command(self):
        raise NotImplementedError()

    def register_with(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self._handle, commands=[self.command])


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
