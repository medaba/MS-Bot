# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class PrivateChatFilter(BoundFilter):
    key = 'is_private'

    def __init__(self, is_private):
        self.is_private = is_private

    async def check(self, message: types.Message):
        return message.chat.type == 'private'
