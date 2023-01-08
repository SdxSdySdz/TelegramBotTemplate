from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from core.handlers import EchoHandler, Handler
from tgbot.config import Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
# from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)

    # register_echo(dp)


async def user_start(message):
    await message.reply("Hello, user!")


class TelegramBot:
    def __init__(self, config):
        self._aiogram_bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
        self._storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
        self._dispatcher = Dispatcher(self._aiogram_bot, storage=self._storage)

        self._aiogram_bot['Config'] = config

        register_all_middlewares(self._dispatcher, config)
        register_all_filters(self._dispatcher)
        # register_all_handlers(self._dispatcher)
        # self._dispatcher.register_message_handler(echo_handler.handle)

    def register_handler(self, handler: Handler):
        handler.register_with(self._dispatcher)

    async def try_start_pooling(self):
        try:
            await self._dispatcher.start_polling()
        finally:
            await self._dispatcher.storage.close()
            await self._dispatcher.storage.wait_closed()
            await self._aiogram_bot.session.close()
