# -*- coding: utf-8 -*-

try:
    import ujson as json
except:
    import json
import asyncio
from aiogram import types

from keyboards import inline_kb, reply_kb
from loader import bot, dp
from states import AnswerToUserForm
from utils.db_api import users_table


@dp.callback_query_handler(answer_user=True)
async def answer_to_user(cb: types.CallbackQuery):
    await cb.message.answer(
        "введите сообщение для ответа юзеру",
        reply_markup=reply_kb.cancel()
    )
    user_id = cb.data.split("answer_user")[1]
    with open('user.json', 'w') as file:
        json.dump({"user_id": user_id}, file, indent=2, ensure_ascii=False)
    await AnswerToUserForm.answer.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'btc')
async def cb_q(cb: types.CallbackQuery):
    await bot.delete_message(
        cb.from_user.id,
        cb.message.message_id
    )
    await asyncio.sleep(0.1)
    await bot.send_photo(
        cb.from_user.id,
        photo="AgACAgIAAxkBAAIcJWAKZzx5EkubNw_-hGuPCmSVoqUPAAKXrzEbdhlQSIwkCPRJjHxU9Ehdmi4AAwEAAwIAA3gAA8-1AwABHgQ",
        caption="Bitcoin: \n\n`bc1q9tsphew7avkzpu8nwp36fjmdsv3vn8mq76pxt8`",
        reply_markup=inline_kb.donate()
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'ltc')
async def cb_q(cb: types.CallbackQuery):
    await bot.delete_message(
        cb.from_user.id,
        cb.message.message_id
    )
    await asyncio.sleep(0.1)
    await bot.send_photo(
        cb.from_user.id,
        photo="AgACAgIAAxkBAAIcI2AKZxI5bUbwHJ8WMBywzV41n_j4AAKWrzEbdhlQSGFwtLkvjxadLrKUly4AAwEAAwIAA3gAAxzvBQABHgQ",
        caption="Litecoin: \n\n`ltc1qxmmjmuvutz5qddeqqyz0v35vc3e75gm688tn9h`",
        reply_markup=inline_kb.donate()
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'eth')
async def cb_q(cb: types.CallbackQuery):
    await bot.delete_message(
        cb.from_user.id,
        cb.message.message_id
    )
    await asyncio.sleep(0.1)
    await bot.send_photo(
        cb.from_user.id,
        photo="AgACAgIAAxkBAAIcIWAKZudsVg8fqSrBFAV6lTzkVFgKAAKVrzEbdhlQSLdag18DN5q36M0smy4AAwEAAwIAA3gAA1ifAQABHgQ",
        caption="Etherium: \n\n`0x6e4a6E3714cc40692d53c94A341c60682095fbc8`",
        reply_markup=inline_kb.donate()
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'xmr')
async def cb_q(cb: types.CallbackQuery):
    await bot.delete_message(
        cb.from_user.id,
        cb.message.message_id
    )
    await asyncio.sleep(0.1)
    await bot.send_photo(
        cb.from_user.id,
        photo="AgACAgIAAxkBAAIcH2AKZqfNgIrWePQtRXRk8gQX9sHEAAKUrzEbdhlQSG5HBFPw7lxyifsamC4AAwEAAwIAA3gAA1v0BQABHgQ",
        caption="Monero: \n\n`8BN7ZCCfdVCg4kjARpStV26jdqPX7FuhfKtGVbACWVi5MSmEDgc99SfFGWSF7zyQTEUWgMPXZQNxeT9f3ccETx2y9sBZJdo`",
        reply_markup=inline_kb.donate()
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'qiwi')
async def cb_q(cb: types.CallbackQuery):
    await bot.delete_message(
        cb.from_user.id,
        cb.message.message_id
    )
    await asyncio.sleep(0.1)
    await cb.message.answer(
        "*QIWI* \n\n"
        "Перевод на qiwi с карты или qiwi-кошелька: "
        "[ССЫЛКА](https://my.qiwi.com/Vyktor-ZgkLrmtvQR?noCache=true)",
        reply_markup=inline_kb.donate(),
        disable_web_page_preview=True
    )


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'yandex')
async def cb_q(cb: types.CallbackQuery):
    await bot.delete_message(
        cb.from_user.id,
        cb.message.message_id
    )
    await asyncio.sleep(0.1)
    await cb.message.answer(
        "Кошелек Yandex.Деньги: \n\n`410012455548219`\n\n",
        reply_markup=inline_kb.donate()
    )
