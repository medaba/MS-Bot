# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config

def source_code():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="👨‍💻 GitHub", url="https://github.com/medaba/MS-Bot"))
    return markup


def donate():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Qiwi", callback_data="qiwi")
    )
    markup.add(
        InlineKeyboardButton(text="Bitcoin", callback_data="btc"),
        InlineKeyboardButton(text="Litecoin", callback_data="ltc"),
        InlineKeyboardButton(text="Etherium", callback_data="eth"),
        InlineKeyboardButton(text="Monero", callback_data="xmr")
    )
    return markup


def answer_to_user(user_id):
    markup = InlineKeyboardMarkup()
    cb_data = f"answer_user{user_id}"
    markup.add(
        InlineKeyboardButton(text='Ответить', callback_data=cb_data))
    return markup

