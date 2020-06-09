from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from main import dp


class PrivateChat(BoundFilter):

    key = "private"

    def __init__(self, private):
        self.private = private

    async def check(self, message: Message) -> bool:
        if message.chat.type == "private":
            return True


dp.filters_factory.bind(PrivateChat)
