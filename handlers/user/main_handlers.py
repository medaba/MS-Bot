# -*- coding: utf-8 -*-

import asyncio
from aiogram.types import Message

import config
import keyboards
from loader import dp, bot
from utils.misc import rate_limit
from utils.db_api import users_table
from utils.misc import logger
from utils.misc.check_distance import calculate_distance
from data.polls_ids import polls_id


@rate_limit(limit=1)
@dp.message_handler(is_private=True, text=["/start", "/restart", "👑 Главное меню"])
async def main_menu(m: Message):
    await m.answer(
        "🤖 *Вы находитесь в главном меню.* \n\n",
        reply_markup=keyboards.reply_kb.main_menu(m)
    )

    try:
        await users_table.fetch_user_by_id(m.from_user.id)        # Получить юзера из БД
        await users_table.activate_user(m.from_user.id)           # Включение статуса active
        await users_table.set_user_polls_page(m.from_user.id, 0)  # Обнуление счетчика страниц опросов
    except:
        # Добавление нового юзера в БД.
        await users_table.add_user(m.from_user.id, m.from_user.full_name, m.from_user.username)
        print(f"Добавлен пользователь: {m.from_user.full_name}, {m.from_user.id}.")
        logger.info(f"Добавлен пользователь: {m.from_user.full_name}, {m.from_user.id}.")


@rate_limit(limit=1)
@dp.message_handler(is_private=True, text=['🤖 О Боте'])
async def info(m: Message):
    await m.answer_photo(
        photo="AgACAgIAAxkBAAIEQV7xyOp4PpNtDS5RPHvCfb0nni9SAAIDrzEbWNOQS5YVAAEyn-HziZ2L5pEuAAMBAAMCAANtAAOpewMAARoE",
        caption="☘️ *Подробнее о боте* \n\n"
                "Данный бот является попыткой собрать в одном месте полезные "
                "ссылки, функции и практические советы для людей, которые столкнулись с Рассеянным склерозом.\n\n"
                "📋 *Краткое содержание бота*:\n"
                "🔸 Блок опросов для сбора статистики.\n"
                "🔸 Обновляющаяся база данных медицинских центров рассеянного склероза.\n"
                "🔸 Поиск ближайшего РС-центра на основе геопозиции пользователя.\n"
                "🔸 Полезные ссылки о РС: телеграм-каналы, сайты, упражнения для реабилитации и т.д.\n"
                "🔸 Инлайн-режим для поиска РС-центров по России. \n",
        parse_mode="Markdown",
        reply_markup=keyboards.reply_kb.about_bot()
    )
 

@rate_limit(limit=1)
@dp.message_handler(is_private=True, text=["☎️ Контакты"])
async def contact(m: Message):
    await m.answer(
        "👨‍💻 *Контакты для связи с разработчиком.* \n\n"
        "Если у вас есть какие-либо замечания или предложения, "
        "вы всегда можете написать на мой рабочий аккаунт: \n\n[ᗩᒪᗷOT](https://t.me/alotofbots)",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


@rate_limit(limit=1)
@dp.message_handler(is_private=True, text=["⚠️ Дисклеймер"])
async def disclaimer(m: Message):
    await m.answer(
        "⚠️ *ДИСКЛЕЙМЕР:*\n\n"
        "Я сам являюсь пациентом и не представляю какие-либо организации или экспертные сообщества. "
        "Помните, что при выборе стратегии лечения стоит полагаться на рекомендации вашего лечащего врача. "
        "Я же в свою очередь могу лишь пожелать вам найти действительно хорошего доктора."
    )


@rate_limit(limit=1)
@dp.message_handler(is_private=True, text=["✅ На витамины"])
async def donation(m: Message):
    await m.answer(
        "Все функции бота предоставляются абсолютно бесплатно. "
        "Но если вдруг у вас появится желание сделать скромное пожертвование"
        ", то реквизиты можно найти прямо под этим сообщением. "
        "\n\nЭто совершенно необязательно, но мне будет как минимум приятно. 😊",
        reply_markup=keyboards.inline_kb.donate()
    )
    

@rate_limit(limit=1)
@dp.message_handler(is_private=True, text=["👨‍💻 Исходный код"])
async def source_code(m: Message):
    await m.answer(
        "*Исходный код проекта:* \n\n"
        "https://github.com/medaba/MS-Bot",
        reply_markup=keyboards.inline_kb.source_code(),
        disable_web_page_preview=True
    )


@rate_limit(limit=1)
@dp.message_handler(is_private=True, text=['💻 Ссылки'])
async def useful_links(m: Message):
    await m.answer(
        '💻 В этом меню собраны ссылки на полезные онлайн-ресурсы о РС, упражнения для реабилитации, ' 
        'телеграм каналы/группы и т.д. \n\n'
        'Если у вас есть какие-либо интересные материалы для "золотой коллекции", '
        'отправляйте их *с кратким описанием* прямо в этот чат.',
        reply_markup=keyboards.reply_kb.links()
    )


@rate_limit(limit=1)
@dp.message_handler(is_private=True, text=['✈️ Телеграм'])
async def rehab(m: Message):
    await m.answer(
        "🔸 [Девочка с РС](https://t.me/ms_girl) - "
        "Переводы статей с англоязычных и немецких источников, результаты исследований и многое другое.\n\n"
        "🔸 [МосОРС](https://t.me/moscowors) - канал московского РС-сообщества (будет полезен не только москвичам).\n\n"
        "🔸 [Библиотека склерозника](https://t.me/biblioteka_skleroznika) - "
        "статьи, книги, видео про РС и о здоровье в целом.\n\n"
        "🔸 [Рассеянный склероз](https://t.me/msneurol) - телеграм-энциклопедия по РС.\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(is_private=True, text=['🌐 Сайты'])
async def rehab(m: Message):
    await m.answer(
        "🔸 [МосОРС](http://mosors.ru/) - сайт Московского РС-сообщества.\n\n"
        "🔸 [SCLEROS.RU](https://scleros.ru/) - информационно-образовательный портал. Новости, форум и т.д.\n\n"
        "🔸 [ОООИ-БРС](https://форум.ооои-брс.рф/) - форум для пациентов с рассеянным склерозом.\n\n"
        "🔸 [G35.CLUB](https://g35.club/) - обзоры зарубежных статей из различных рецензируемых мед. журналов.\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(is_private=True, text=['🗂️ Разное'])
async def other(m: Message):
    await m.answer(
        "🔸 [Школа пациента (YouTube - МосОРС)](https://www.youtube.com/watch?v=FJ6WTcU-f3w&list=PLYhtMe98iobYeKgSScUwxoTKIEz8fA0Gl) - YouTube плейлист.\n\n"
        "🔸 [Калькулятор EDSS](http://edss.neurol.ru/edss_ru/) - онлайн калькулятор. "
        "для оценки степени инвалидизации пациентов с РС. Версия для врачей неврологов.\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(is_private=True, text=['♥️ Реабилитация'])
async def rehab(m: Message):
    await m.answer(
        "*Упражнения для реабилитации. Курс молодого бойца* ️🤺️\n\n"
        "Упражнения, рекомендуемые при рассеянном склерозе, "
        "позволяют замедлить прогрессирование процесса и заметно улучшить общее состояние. \n\n\n"
        "🔸 Комплекс домашних упражнений для бодрости и поднятия боевого духа: "
        "[YouTube/Плейлист](https://www.youtube.com/watch?v=A1wB3qlhzRI&list=PLq3gpRvKC5jbuzKD61X6YIfBdKcGO30EJ)\n\n"
        "🔸 Подборка разминочных упражнений: "
        "[YouTube](https://www.youtube.com/watch?v=HC15GNT9FkY)\n\n"
        "🔸 Развитие мелкой моторики пальцев: "
        "[YouTube/ENG](https://www.youtube.com/watch?v=sB4lXUhRfMU&feature=youtu.be)\n\n"
        # "🔸 Упражнение с веревкой: "
        # "[Пошаговая инструкция (YouTube)](https://www.youtube.com/watch?v=isWWtIwdiQE)\n\n"
        "🔸 10 упражнений для стоп: [сайт/текст с картинками](https://mednew.site/sport/10-uprazhnenij-dlya-stop)\n\n"
        "🔸 Упражнения на координацию из программы подготовки летчиков: [видео](https://t.me/mscler/39573)\n\n"
        "🔸 Упражнения для вестибулярного аппарата: "
        "[сайт/текст с картинками](https://vladmedicina.ru/persons/p52698.htm)\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(is_private=True, text=['📜 Опросы'])
async def polls(m: Message):
    await m.answer(
        "📃 *Блок опросов для пациентов c Рассеянным склерозом* \n\n"
        "Если болеете не вы, а ваш близкий, то допускается голосование от его лица. \n\n"
        "Вы всегда можете отменить свой голос и переголосовать заново.\n\n\n"
        "Чтобы начать нажмите кнопку 'Вперед' ▶",
        reply_markup=keyboards.reply_kb.polls_navigation()
    )


@dp.message_handler(is_private=True, text=["Вперед ▶️"])
async def info(m: Message):
    current_polls_page = await users_table.get_user_polls_page(m.from_user.id)
    next_page = current_polls_page + 1
    if next_page <= len(polls_id):
        poll_id = polls_id[next_page]
        await bot.forward_message(m.from_user.id, 698425366, poll_id)
        await users_table.set_user_polls_page(m.from_user.id, next_page)
    elif next_page > len(polls_id):
        await m.answer(
            "❤️️ Конец блока опросов. Спасибо за участие 🙏"
        )


@dp.message_handler(is_private=True, text=["◀️ Назад"])
async def info(m: Message):
    current_polls_page = await users_table.get_user_polls_page(m.from_user.id)
    previous_page = current_polls_page - 1
    if previous_page > 0:
        poll_id = polls_id[previous_page]
        await bot.forward_message(m.from_user.id, 698425366, poll_id)
        await users_table.set_user_polls_page(m.from_user.id, previous_page)
    elif previous_page <= 0:
        await users_table.set_user_polls_page(m.from_user.id, 0)
        await polls(m)


@dp.message_handler(is_private=True, text=['🧑‍⚕️ РС-Центры'])
async def main_msc(m: Message):
    await m.answer(
        "🏥 Данное меню поможет вам найти РС-Центр в вашем городе (РФ) \n\n"
        "Если вы обнаружили, что в базе не хватает какого-либо *специализированного* РС-центра, "
        "*который ведет прием пациентов по ОМС*, "
        "отправьте пожалуйста название и адрес этой организации прямо в этот чат.",
        reply_markup=keyboards.reply_kb.msc()
    )


@dp.message_handler(is_private=True, text=['🌍 Все центры'])
async def show_all_msc(m: Message):
    await m.answer(
        "*Список Центров Рассеянного Склероза* \n\n"
        f"[TELEGRA.PH]({config.MS_CENTERS})"
    )


@dp.message_handler(is_private=True, content_types=['location'])
async def proc_location(m: Message):
    user_coords = (m.location.latitude, m.location.longitude)  # координаты пользователя
    try:
        await users_table.save_location(m.from_user.id, user_coords)
    except Exception as e:
        print(e)

    best_distance, best_address = await calculate_distance(user_coords)

    await bot.delete_message(
        m.chat.id,
        m.message_id)

    await bot.send_venue(
        m.chat.id,
        best_address[4],
        best_address[5],
        best_address[3],
        best_address[2])

    await asyncio.sleep(1)

    answer = ", ".join(best_address[:4])
    await m.answer(
        "Ближайший от вас Центр Рассеянного Cклероза находится по адресу: \n\n"
        f"🔸 {answer} \n\n"
        f"🚁 Расстояние: {round(best_distance.km, 1)} км.")


@dp.message_handler(is_private=True, content_types=['contact'])
async def contact_proc(m: Message):
    await users_table.save_phone(m.from_user.id, m.contact.phone_number)

