# -*- coding: utf-8 -*-

import asyncio
from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

try:
    import ujson as json
except:
    import json

import config
import keyboards
from loader import dp, bot
from handlers.user.start import main_menu
from states import MailingForm, MsgToAdminForm, AnswerToUserForm
from utils.db_api import users_table
from utils.misc import mailing


@dp.message_handler(state=MailingForm.mail_msg)
async def process_mailing_message(m: Message, state: FSMContext):
    """
    Обрабатывает принятый State с сообщением для рассылки и
    запускает рассылку.
    """
    all_users = await users_table.fetch_all_active_users()
    await mailing.start_mailing(admin_id=m.from_user.id,
                                users_ids=all_users,
                                text=m.text)
    await state.finish()


@dp.message_handler(state=MsgToAdminForm.msg_to_admin)
async def process_msg_to_admin(m: Message, state: FSMContext):
    await state.finish()
    if m.text == "Отмена 🚫":
        await main_menu(m)
        return
    elif m.text == "✅ Отправить":
        msg_id = await users_table.get_saved_message_id(m.from_user.id)

        await bot.forward_message(config.MAIN_ADMIN, m.chat.id, msg_id)

        await asyncio.sleep(0.2)
        await bot.send_message(
            config.MAIN_ADMIN,
            f"Сообщение от пользователя {m.from_user.id}",
            reply_markup=keyboards.inline_kb.answer_to_user(m.from_user.id)
        )

        await asyncio.sleep(1)
        await m.answer('✅ Ваше сообщение передано администратору',
                       reply_markup=keyboards.reply_kb.main_menu(m))


@dp.message_handler(state=AnswerToUserForm.answer)
async def process_answer_to_user(m: Message, state: FSMContext):
    if m.text != "🚫 Отмена":
        user_id = json.load(open('user.json'))["user_id"]
        await bot.send_message(
            user_id,
            m.text
        )
    await state.finish()
    await main_menu(m)
