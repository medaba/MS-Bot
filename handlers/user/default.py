# -*- coding: utf-8 -*-

from aiogram.types import Message

import config
from loader import bot, dp
from utils.misc import rate_limit
import keyboards


@rate_limit(limit=1)
@dp.message_handler(is_private=True, commands="getbot", user_id=config.ADMINS)
async def getbot(m: Message):
    bot_info = await bot.get_me()
    bot_info = bot_info.to_python()
    await m.answer(
        f"ID: {bot_info['id']}\n"
        f"Bot\'s name: {bot_info['first_name']}\n"
        f"Bot\'s username: @{bot_info['username']}\n"
        f"Can join groups: {bot_info['can_join_groups']}\n"
        f"Can read group messages: {bot_info['can_read_all_group_messages']}\n"
        f"Inline queries: {bot_info['supports_inline_queries']}\n"
    )


@rate_limit(limit=1)
@dp.message_handler(is_private=True, commands="creator")
async def creator(m: Message):
    await m.answer(
        f'Creator: {config.CREATOR}'
    )


@rate_limit(limit=1)
@dp.message_handler(is_private=True, commands="myid")
async def my_id(m: Message):
    await m.answer(
        f"Ваш User ID: `{m.from_user.id}`",
        parse_mode='Markdown'
    )
