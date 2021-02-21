# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.types import InlineQuery

from loader import dp
from utils.db_api import mscenter_table


@dp.inline_handler()
async def inlinequery(query: InlineQuery):
    city = query.query
    answer = await create_answer(city)

    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="unknown",
                thumb_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/96/hospital_1f3e5.png",
                title=f"🏥 РС-центры в городе: {city}",
                input_message_content=types.InputMessageContent(
                    message_text=answer,
                    parse_mode="Markdown"
                )
            )
        ],
    )


async def create_answer(city):
    msc_list = await mscenter_table.fetch_all_msc_in_city(city)
    answer = f"🏥 *РС-центры в городе: {city}*\n\n"

    if not msc_list:
        answer += "Не найдено"
    else:
        for msc in msc_list:
            answer += f"🔸 {msc[2]}\nАдрес: {msc[3]}\n\n"

    return answer
