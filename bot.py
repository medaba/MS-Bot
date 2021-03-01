# -*- coding: utf-8 -*-

from aiogram import executor

from loader import bot, dp
from utils.set_bot_commands import set_bot_commands
from utils.notify_admins import on_startup_notify
from utils.misc import logger


async def on_startup(*args):
    import middlewares
    middlewares.setup(dp)
    import filters
    filters.setup(dp)

    import handlers

    await on_startup_notify()
    await set_bot_commands(dp)
    print("bot launched")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True, reset_webhook=True)
