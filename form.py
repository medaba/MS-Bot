# -*- coding: utf-8 -*-

from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    message_template = State()  # Будет представленно в хранилище как 'message_template'
    message_for_admin = State()