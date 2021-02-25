# -*- coding: utf-8 -*-

from aiogram import types


async def set_bot_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "- запустить/перезапустить бота")]
    )
