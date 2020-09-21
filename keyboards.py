# -*- coding: utf-8 -*-

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(
        KeyboardButton("📜 Опросы"),
        KeyboardButton("🔗 Ссылки"),

    ).add(
        KeyboardButton("🤖 О Боте"),
        KeyboardButton("🧑‍⚕️ РС-Центры")
    )
    return markup


def links():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("✈️ Телеграм"),
        KeyboardButton("🌐 Сайты")
    ).add(
        ("♥️ Реабилитация")
    ).add(
        KeyboardButton("👑 Главное меню")
    )
    return markup


def contacts():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton(text="✅ Разработчику на витамины"),
        KeyboardButton("👑 Главное меню")
    )
    return markup


def source_code():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="👨‍💻 GitHub", url="https://github.com/medaba/MS-Bot"))
    return markup


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
        KeyboardButton("Отмена"),
        KeyboardButton("👑 Главное меню")
    )
    return markup


def about_bot():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    # markup.add(
    #     KeyboardButton("📃 Инструкция"))
    markup.add(
        KeyboardButton("☎️ Контакты"),
        KeyboardButton("⚠️ Дисклеймер"),
        KeyboardButton("👨‍💻 Исходный код"),
        KeyboardButton("👾 QR-ссылка")
    ).add(
        KeyboardButton("👑 Главное меню")
    )
    return markup


def polls_navigation():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("◀️ Назад"),
        KeyboardButton("Вперед ▶️")
    )
    markup.add(
        KeyboardButton("👑 Главное меню"))
    return markup
