import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from core.handlers import EchoHandler, CommandStartHandler
from core.bot import TelegramBot, register_all_middlewares, register_all_filters, register_all_handlers
from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting core")
    config = load_config(".env")

    if True:
        bot = TelegramBot(config)

        bot.register_handler(CommandStartHandler())
        bot.register_handler(EchoHandler())

        await bot.try_start_pooling()
    else:
        storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
        bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
        dp = Dispatcher(bot, storage=storage)

        bot['config'] = config

        register_all_middlewares(dp, config)
        register_all_filters(dp)
        register_all_handlers(dp)

        # start
        try:
            await dp.start_polling()
        finally:
            await dp.storage.close()
            await dp.storage.wait_closed()
            await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
