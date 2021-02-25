# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import InlineQuery

from loader import dp
from utils.db_api import mscenter_table, all_city_names


@dp.inline_handler(Text(all_city_names, ignore_case=True))
async def show_msc_in_city(query: InlineQuery):
    city = query.query.title()
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


@dp.inline_handler(regexp="\w")
async def show_msc(query: InlineQuery):
    city = query.query.title()

    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="unknown",
                thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_button_cancel.svg/150px-Crystal_button_cancel.svg.png",
                title=f"🚫 РС-центры в городе {city} не найдены",
                input_message_content=types.InputMessageContent(
                    message_text=f"🚫 РС-центры в городе {city} не найдены",
                    parse_mode="Markdown"
                )
            )
        ],
    )


async def create_answer(city):
    msc_list = await mscenter_table.fetch_all_msc_in_city(city)
    answer = f"🏥 *РС-центры в городе: {city}*\n\n"

    if not msc_list:
        answer += "🚫 Не найдено"
    else:
        for msc in msc_list:
            answer += f"🔸 {msc[2]}\nАдрес: {msc[3]}\n\n"

    return answer
