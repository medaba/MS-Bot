# -*- coding: utf-8 -*-

import aiogram

import config
from utils.misc.logger import logger


async def on_startup_notify(dp: aiogram.Dispatcher):
    try:
        await dp.bot.send_message(
            chat_id=config.MAIN_ADMIN,
            text="Бот запущен"
        )
    except Exception as e:
        print(e)
        logger.error(e)
