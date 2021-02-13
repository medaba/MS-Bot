# -*- coding: utf-8 -*-

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import Message

import config


def main_menu(m: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🤖 О Боте"),
        KeyboardButton('💻 Ссылки'),
        KeyboardButton("🧑‍⚕️ РС-Центры"),
        KeyboardButton("📜 Опросы")
    )
    if m.from_user.id in config.ADMINS:
        markup.add(
            KeyboardButton("✉️ Рассылка")
        )
    return markup


def links():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("✈️ Телеграм"),
        KeyboardButton("🌐 Сайты"),
        KeyboardButton("♥️ Реабилитация"),
        KeyboardButton('🗂️ Разное')
    ).add(
        KeyboardButton("👑 Главное меню")
    )
    return markup


# def contacts():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(
#         KeyboardButton("👑 Главное меню")
#     )
#     return markup


def msc():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌍 Все центры"),
        KeyboardButton("📌 Ближайший", request_location=True),
        KeyboardButton("👑 Главное меню")
    )
    return markup


def canceling():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton("🚫 Отмена"),
        KeyboardButton("👑 Главное меню")
    )
    return markup


def cancel():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🚫 Отмена")
    )
    return markup


def message_for_admin_yes_no():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("✅ Отправить"),
        KeyboardButton("Отмена 🚫")
    )
    return markup


def about_bot():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("☎️ Контакты"),
        KeyboardButton("👨‍💻 Исходный код"),
        KeyboardButton("✅ На витамины"),
        KeyboardButton(text="⚠️ Дисклеймер")
    ).add(
        KeyboardButton("👑 Главное меню")
    )
    return markup


def polls_navigation():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("◀️ Назад"),
        KeyboardButton("Вперед ▶️"),
        KeyboardButton("👑 Главное меню"))
    return markup
