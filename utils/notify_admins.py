# -*- coding: utf-8 -*-

from aiogram.types import Message

import config
from loader import bot
from utils.misc.logger import logger


async def on_startup_notify():
    try:
        await bot.send_message(
            chat_id=config.MAIN_ADMIN,
            text="Бот запущен"
        )
    except Exception as e:
        print(e)
        logger.error(e)


async def donate_notify(m: Message):
    await bot.send_message(
        config.MAIN_ADMIN,
        f"Пользователь {m.from_user.full_name} {m.from_user.id} запросил реквизиты для доната."
    )


async def new_user_notify(m: Message):
    await bot.send_message(
        config.MAIN_ADMIN,
        f"Новый пользователь {m.from_user.full_name} {m.from_user.id}"
    )
