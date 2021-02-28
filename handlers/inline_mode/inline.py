# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.dispatcher.filters.builtin import Text
from aiogram.types import InlineQuery

import config
from keyboards import inline_kb
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
    city: str = query.query.title()
    results = []

    for city_name in all_city_names:
        if city_name.lower().startswith(city.lower()):
            answer = await create_answer(city_name)
            results.append(
                types.InlineQueryResultArticle(
                    id=f"{city_name}",
                    thumb_url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/160/apple/96/hospital_1f3e5.png",
                    title=f"🏥 РС-центры в городе: {city_name}",
                    input_message_content=types.InputTextMessageContent(
                        message_text=answer,
                        parse_mode="HTML",
                        disable_web_page_preview=True
                    ),
                    reply_markup=inline_kb.bot_link()
                )
            )

    if not results:
        results.append(
            types.InlineQueryResultArticle(
                id=f"{city}",
                thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_button_cancel.svg/150px-Crystal_button_cancel.svg.png",
                title=f"🚫 Подходящие РС-центры не найдены",
                input_message_content=types.InputTextMessageContent(
                    message_text="🏥 Открытая база медицинских центров, занимающихся вопросами Рассеянного склероза:\n"
                                 f"[База РС-Центров]({config.MS_CENTERS})\n\n"
                                 f"✅ Еще больше полезных функций вы сможете найти в приватном чате бота.\n\n"
                                 "⚠️Если вы обнаружили, что в базе не хватает какого-либо *специализированного* РС-центра,"
                                 "*который ведет прием пациентов по ОМС*, отправьте пожалуйста адрес и название этой "
                                 f"организации в ЛС боту.",
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                ),
                reply_markup=inline_kb.bot_link()
            )
        )

    await query.answer(
        results=results
    )


async def create_answer(city):
    msc_list = await mscenter_table.fetch_all_msc_in_city(city)
    answer = f"🏥 <b>РС-центры в городе: {city}</b>\n\n"

    if not msc_list:
        answer += "🚫 Не найдено"
    else:
        for msc in msc_list:
            answer += f"🔸 {msc[2]}\nАдрес: {msc[3]}\n\n"
        answer += f"✅ Еще больше полезных функций вы сможете найти в приватном чате бота:"

    return answer
