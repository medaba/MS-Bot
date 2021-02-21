# -*- coding: utf-8 -*-

import asyncio
from aiogram.types import Message

import keyboards
from states import MsgToAdminForm
from loader import dp, bot
from utils.db_api import users_table


@dp.message_handler(is_private=True)
async def all_messages(m: Message):
    """
    Хэндлер для всех остальных сообщений. Пересылает сообщение администратору бота
    """
    await users_table.save_last_msg_id(m.from_user.id, m.message_id)
    await m.answer('️👆 Отправить сообщение администратору бота?',
                   reply_markup=keyboards.reply_kb.message_for_admin_yes_no())
    await MsgToAdminForm.msg_to_admin.set()
