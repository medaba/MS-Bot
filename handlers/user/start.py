# -*- coding: utf-8 -*-

from aiogram.types import Message, ChatType

import keyboards
from loader import dp
from utils.misc import rate_limit
from utils.misc import logger
from utils.db_api import users_table


async def main_menu(m: Message):
    await m.answer(
        "🤖 *Вы находитесь в главном меню.* \n\n",
        reply_markup=keyboards.reply_kb.main_menu(m)
    )

    try:
        await users_table.fetch_user_by_id(m.from_user.id)        # Получить юзера из БД
        await users_table.activate_user(m.from_user.id)         # Включение статуса active
        await users_table.set_user_polls_page(m.from_user.id, 0)  # Обнуление счетчика страниц опросов
    except:
        # Добавление нового юзера в БД.
        await users_table.add_user(m.from_user.id, m.from_user.full_name, m.from_user.username)
        print(f"Добавлен пользователь: {m.from_user.first_name}, {m.from_user.id}.")
        logger.info(f"Добавлен пользователь: {m.from_user.first_name}, {m.from_user.id}.")


@rate_limit(limit=1)
@dp.message_handler(commands="start")
async def bot_start(m: Message):
    await main_menu(m)


@rate_limit(limit=1)
@dp.message_handler(is_private=True, text="👑 Главное меню")
async def show_main_menu(m: Message):
    await main_menu(m)
