# -*- coding: utf-8 -*-

import asyncio
from aiogram.types import Message

from keyboards import reply_kb
from states import MailingForm
from loader import dp, bot


@dp.message_handler(text="✉️ Рассылка", is_private=True, is_admin=True)
async def start_mailing(m: Message):
    await m.answer(
        "Отправьте мне сообщение для рассылки",
        reply_markup=reply_kb.canceling()
    )
    await MailingForm.mail_msg.set()
