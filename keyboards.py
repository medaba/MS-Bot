# -*- coding: utf-8 -*-

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🤖 О Боте"),
        KeyboardButton("📜 Опросы"),
        KeyboardButton("🔗 Ссылки"),
        KeyboardButton("🧑‍⚕️ РС-Центры"),
        KeyboardButton("♥️ Реабилитация")
    )
    return markup


def contacts():
    markup = InlineKeyboardMarkup(resize_keyboard=True)
    markup.add(
        InlineKeyboardButton(text="✅ Разработчику на витамины", callback_data="D3")
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


def about_bot():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("☎️ Контакты"),
        KeyboardButton("📃 Инструкция")
    ).add(
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
    markup.add(KeyboardButton("⏮️ Начало опросов"))
    markup.add(KeyboardButton("👑 Главное меню"))
    return markup
