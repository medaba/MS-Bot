# -*- coding: utf-8 -*-

import asyncio
import logging
import ujson as json

from aiogram import types
from aiogram.types import Message, ChatType
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import utils
import keyboards
import mailing
from check_distance import calculate_distance
from form import Form
from database import AioSQLiteWrapper
from polls_ids import polls_id


logging.basicConfig(
    level=logging.INFO,
    filename='logger.log',
    filemode='a',
    format='%(asctime)s | %(name)s | %(levelname)-4s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

logger = logging.getLogger()

bot = Bot(token=config.token, parse_mode="Markdown")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def startup(*args):
    try:
        await bot.send_message(chat_id=config.main_admin, text="База, я на связи ✅")
    except Exception as e:
        print(e)


async def shutdown(*args):
    try:
        await bot.send_message(chat_id=config.main_admin, text="Бот остановлен ❌")
    except Exception as e:
        print(e)


async def main_menu(m: Message):
    await m.answer(
        "🤖 *Вы находитесь в главном меню.* \n\n",
        reply_markup=keyboards.main_menu()
    )

    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    try:
        await users_table.fetch_user_by_id(m.from_user.id)        # Получить юзера из БД
        await users_table.set_user_active(m.from_user.id)         # Включение статуса active
        await users_table.set_user_polls_page(m.from_user.id, 0)  # Обнуление счетчика страниц опросов
    except:
        # Добавление нового юзера в БД.
        await users_table.add_row("(user_id, first_name, last_name, username)",
                                  f"({m.from_user.id}, '{m.from_user.first_name}', '{m.from_user.last_name}', '{m.from_user.username}')")
        print(f"Добавлен пользователь: {m.from_user.first_name}, {m.from_user.id}.")
        logger.info(f"Добавлен пользователь: {m.from_user.first_name}, {m.from_user.id}.")


@dp.message_handler(ChatType.is_private, commands=['start'])
async def start(m: Message):
    await main_menu(m)


# @dp.message_handler(ChatType.is_private)
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


@dp.message_handler(ChatType.is_private, text="👑 Главное меню")
async def show_main_menu(m: Message):
    await main_menu(m)


@dp.message_handler(ChatType.is_private, text=['🤖 О Боте'])
async def info(m: Message):
    await m.answer(
        "☘️ *Подробнее о боте* \n\n"
        "🛠️ Бот создан с целью предоставления дополнительной информации и некоторых полезных функций"
        " для людей, столкнувшихся с рассеянным склерозом.\n\n",
        reply_markup=keyboards.about_bot()
    )


@dp.message_handler(ChatType.is_private, text=["⚠️ Дисклеймер"])
async def info(m: Message):
    await m.answer(
        "⚠️ *ДИСКЛЕЙМЕР:*\n\n"
        "Данный бот является попыткой собрать в одном месте полезные "
        " ссылки, функции и практические советы для людей, которые столкнулись с РС. "
        "Сам я такой же пациент и не представляю какие-либо организации или экспертные сообщества. "
        "Помните, что при выборе стратегии лечения стоит полагаться на рекомендации вашего лечащего врача, "
        "а я в свою очередь могу лишь пожелать вам найти действительно хорошего доктора.",
        reply_markup=keyboards.about_bot()
    )


@dp.message_handler(ChatType.is_private, text=["☎️ Контакты"])
async def contact(m: Message):
    await m.answer(
        "👨‍💻 *Контакты для связи с разработчиком:* \n\n"
        "Если у вас есть какие-либо замечания или предложения, "
        "то вы всегда можете написать на мой рабочий аккаунт: \n\n[BOTSFAM](https://t.me/alotofbots)",
        parse_mode="Markdown",
        reply_markup=keyboards.contacts(),
        disable_web_page_preview=True
    )


@dp.message_handler(ChatType.is_private, text=["✅ Разработчику на витамины"])
async def donate(m: Message):
    await m.answer(
        "*Карта* (QIWI/VISA): `4693 9575 5871 1698` \n\n"
        "*QIWI* перевод по никнейму: https://qiwi.com/n/SUNNYDAY\n\n"
        "*Yandex.Деньги:* `410012455548219`",
        reply_markup=keyboards.contacts()
    )


@dp.message_handler(ChatType.is_private, text=["👾 QR-ссылка"])
async def qr(m: Message):
    await m.answer_photo(
        photo="AgACAgIAAxkBAAIEQV7xyOp4PpNtDS5RPHvCfb0nni9SAAIDrzEbWNOQS5YVAAEyn-HziZ2L5pEuAAMBAAMCAANtAAOpewMAARoE",
        caption=r"🟠 https://t.me/g35_robot",
        parse_mode="HTML"
    )


@dp.message_handler(ChatType.is_private, text=["👨‍💻 Исходный код"])
async def source_code(m: Message):
    await m.answer(
        "*Исходный код проекта:* \n\n"
        "https://github.com/medaba/MS-Bot",
        reply_markup=keyboards.source_code(),
        disable_web_page_preview=True
    )


@dp.message_handler(ChatType.is_private, text=['💻 Ссылки'])
async def useful_links(m: Message):
    await m.answer(
        'В этом меню собраны ссылки на полезные онлайн-ресурсы о РС, упражнения для реабилитации, ' 
        'телеграм каналы/группы и т.д. \n\n'
        'Если у вас есть какие-либо интересные материалы, отправляйте их *с кратким описанием* прямо в этот чат.',
        reply_markup=keyboards.links()
    )


@dp.message_handler(ChatType.is_private, text=['✈️ Телеграм'])
async def rehab(m: Message):
    await m.answer(
        "🔸 [Девочка с РС](https://t.me/ms_girl) - "
        "Переводы статей с англоязычных и немецких источников, результаты исследований и многое другое.\n\n"
        "🔸 [МосОРС](https://t.me/moscowors) - канал московского РС-сообщества (будет полезен не только москвичам).\n\n"
        "🔸 [Библиотека склерозника](https://t.me/biblioteka_skleroznika) - "
        "статьи, книги, видео про РС и о здоровье в целом.\n\n"
        "🔸 [Рассеянный склероз](https://t.me/msneurol) - телеграм-энциклопедия по РС.\n\n"
        "🔸 [G35](https://t.me/mscler) - канал для общения на темы связанные с РС.\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(ChatType.is_private, text=['🌐 Сайты'])
async def rehab(m: Message):
    await m.answer(
        "🔸 [МосОРС](http://mosors.ru/) - сайт Московского РС-сообщества.\n\n"
        "🔸 [SCLEROS.RU](https://scleros.ru/) - информационно-образовательный портал. Новости, форум и т.д.\n\n"
        "🔸 [ОООИ-БРС](https://форум.ооои-брс.рф/) - форум для пациентов с рассеянным склерозом.\n\n"
        "🔸 [G35.CLUB](https://g35.club/) - обзоры зарубежных статей из различных рецензируемых мед. журналов.\n\n"
        "🔸 [NEUROL.RU](http://neurol.ru/) - сайт Казанского РС-центра.\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(ChatType.is_private, text=['🗂️ Разное'])
async def other(m: Message):
    await m.answer(
        "🔸 [Калькулятор EDSS](http://edss.neurol.ru/edss_ru/) - онлайн калькулятор. "
        "для оценки степени инвалидизации пациентов с РС. Версия для врачей неврологов.\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(ChatType.is_private, text=['♥️ Реабилитация'])
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
        "[сайт/текст с картинками](https://vladmedicina.ru/persons/p52698.htm)\n\n"
        "🔸 [Школа пациента (YouTube - МосОРС)](https://www.youtube.com/watch?v=FJ6WTcU-f3w&list=PLYhtMe98iobYeKgSScUwxoTKIEz8fA0Gl) - YouTube плейлист.\n\n",
        disable_web_page_preview=True
    )


@dp.message_handler(ChatType.is_private, text=['📜 Опросы'])
async def polls(m: Message):
    await m.answer(
        "📃 *Блок опросов для людей c Рассеянным склерозом* \n\n"
        "Если болеете не вы, а ваш близкий, то допускается голосование от его лица. \n\n"
        "Вы всегда можете отменить свой голос и переголосовать заново.\n\n\n"
        "Чтобы начать нажмите кнопку 'Вперед' ▶",
        reply_markup=keyboards.polls_navigation()
    )


@dp.message_handler(ChatType.is_private, text=['🧑‍⚕️ РС-Центры'])
async def main_msc(m: Message):
    await m.answer(
        "🏥 Данное меню поможет вам найти РС-Центр в вашем городе (РФ) \n\n"
        "Если вы обнаружили, что в базе не хватает какого-либо *специализированного* РС-центра, "
        "который *ведет прием пациентов по ОМС*, смело отправляйте название и адрес прямо в этот чат.",
        reply_markup=keyboards.msc()
    )


@dp.message_handler(ChatType.is_private, text=['🌍 Все центры'])
async def show_all_msc(m: Message):
    await m.answer(
        "*Список Центров Рассеянного Склероза* \n\n"
        '[telegra.ph](https://telegra.ph/Spisok-RS-Centrov-06-08-19) | '
        '[зеркало](https://tgraph.io/Spisok-RS-Centrov-06-08-19)'
    )


@dp.message_handler(ChatType.is_private, content_types=['location'])
async def proc_location(m: Message):
    user_coords = (m.location.latitude, m.location.longitude)  # координаты пользователя
    try:
        users_table = AioSQLiteWrapper("g35.sqlite", table_name="users")
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


@dp.message_handler(ChatType.is_private, content_types=['contact'])
async def contact_proc(m: Message):
    users_table = AioSQLiteWrapper("g35.sqlite", table_name="users")
    await users_table.save_phone(m.from_user.id, m.contact.phone_number)


@dp.message_handler(ChatType.is_private, text=["Вперед ▶️"])
async def info(m: Message):
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
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


@dp.message_handler(ChatType.is_private, text=["◀️ Назад"])
async def info(m: Message):
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    current_polls_page = await users_table.get_user_polls_page(m.from_user.id)
    previous_page = current_polls_page - 1
    if previous_page > 0:
        poll_id = polls_id[previous_page]
        await bot.forward_message(m.from_user.id, 698425366, poll_id)
        await users_table.set_user_polls_page(m.from_user.id, previous_page)
    elif previous_page <= 0:
        users_table = AioSQLiteWrapper("g35.sqlite", "users")
        await users_table.set_user_polls_page(m.from_user.id, 0)
        await polls(m)


@dp.message_handler(ChatType.is_private, text=["⏮️ Начало опросов"])
async def info(m: Message):
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    await users_table.set_user_polls_page(m.from_user.id, 0)
    await polls(m)


@dp.message_handler(ChatType.is_private, commands=['mailing'])
async def start_mailing(m: Message):
    if m.from_user.id in config.admins:
        await m.answer(
            "Отправьте мне сообщение для рассылки",
            reply_markup=keyboards.canceling()
        )
        await Form.message_template.set()


@dp.message_handler(state=Form.message_template)
async def process_msg_template(m: Message, state: FSMContext):
    """
    Обрабатывает принятый State с сообщением для рассылки и
    запускает рассылку.
    """
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    all_users = await users_table.fetch_all_active_users()
    all_users_ids = await users_table.get_all_users_ids(all_users)
    await mailing.start_mailing(admin_id=m.from_user.id,
                                users_ids=all_users_ids,
                                text=m.text)
    await state.finish()


@dp.message_handler(ChatType.is_private, commands=['g35'])
async def say_to_g35(m: Message):
    """
    Сказать от имени бота в G35
    """
    if m.from_user.id in config.admins:
        text = utils.edit_cmd(m.text)
        await bot.send_message(
            config.matests,
            text
        )
        await bot.send_animation(
            chat_id=config.matests,
            animation="AAMCAgADGQEAAhqvXueMLoIs36dZrmU_cI1hrYoRBoQAAkMGAAKdpiFJRp2_h30a5ePbScoOAAQBAAdtAAO2fAACGgQ"
        )


@dp.message_handler(commands=['myid'])
async def my_id(m: Message):
    """
    Отправляет пользователю его ID в телеграме
    """
    await m.reply(
        "Ваш ID 👇 \n\n"
        f"`{m.from_user.id}`"
    )


@dp.message_handler(commands=['creator'])
async def show_creator(m: Message):
    """
    Отправить сообщение с username создателя бота (config.creator)
    """
    await m.answer(
        f'Меня создал {config.creator}'
    )


@dp.message_handler(ChatType.is_private, content_types=['photo'])
async def get_photo_id(m: Message):
    """
    Возвращает админу бота ID отправленного фото.
    """
    if m.from_user.id in config.admins:
        await m.answer(
            f"`{m.photo[-1]['file_id']}`",
            parse_mode=None
        )


@dp.message_handler(state=Form.message_for_admin)
async def process_msg_to_admin(m: Message, state: FSMContext):
    await state.finish()
    if m.text == "Отмена 🚫":
        await main_menu(m)
        return
    elif m.text == "✅ Отправить":
        users_table = AioSQLiteWrapper("g35.sqlite", "users")
        msg_id = await users_table.get_saved_message_id(m.from_user.id)
        await bot.forward_message(config.main_admin, m.chat.id, msg_id)
        await asyncio.sleep(1)
        await m.answer('✅ Ваше сообщение передано администратору',
                       reply_markup=keyboards.main_menu())


@dp.message_handler(ChatType.is_private)
async def all_messages(m: Message):
    """
    Хэндлер для всех остальных сообщений. Пересылает сообщение администратору бота
    """
    users_table = AioSQLiteWrapper("g35.sqlite", "users")
    await users_table.save_last_msg_id(m.from_user.id, m.message_id)
    await m.answer('️👆 Отправить сообщение администратору бота?',
                   reply_markup=keyboards.message_for_admin_yes_no())
    await Form.message_for_admin.set()



async def i_am_alive(sleep_for=28800):
    """
    Периодическая ф-я.
    Отправляет админу сообщение о своей работоспособности каждые 'sleep_for' секунд.
    """
    while True:
        await asyncio.sleep(sleep_for)  # Пауза. Цикл замирает на sleep_for секунд
        await bot.send_message(
            config.main_admin,
            "I am alive ",
            disable_notification=True
        )


if __name__ == '__main__':
    dp.loop.create_task(i_am_alive())

    if config.webhook is False:
        executor.start_polling(dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown, relax=0.5)
