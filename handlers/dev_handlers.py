# -*- coding: utf-8 -*-

from aiogram.types import Message

from loader import bot, dp


@dp.message_handler(is_private=True, not_admin=True)
async def non_dev(m: Message):
    await m.answer(
        "👨‍💻 Ведутся технические работы, попробуйте повторить запрос позднее."
    )


# @dp.message_handler(is_private=True)
# async def send_json(m: Message):
#     """
#     На любое сообщение отвечает сырым JSON-ом
#     """
#     print(str(m.as_json()))
#     await bot.send_message(
#         m.chat.id,
#         str(m.as_json()),
#         parse_mode='HTML'
#     )


@dp.message_handler(is_admin=True, is_private=True, content_types=['photo'])
async def get_photo_id(m: Message):
    """
    Возвращает админу бота ID отправленного фото.
    """
    await m.answer(
        f"`{m.photo[-1]['file_id']}`",
        parse_mode="Markdown"
    )
