# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AnswerToUserFilter(BoundFilter):
    key = 'answer_user'

    def __init__(self, answer_user):
        self.answer_user = answer_user

    async def check(self, cb: types.CallbackQuery):
        return "answer_user" in cb.data