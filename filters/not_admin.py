# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import config


class NotAdminFilter(BoundFilter):
    key = 'not_admin'

    def __init__(self, not_admin):
        self.not_admin = not_admin

    async def check(self, message: types.Message):
        if message.from_user.id not in config.ADMINS:
            return True
